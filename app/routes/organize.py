from flask import Blueprint, request, render_template

from app.core.scanner import Scanner
from app.services.organizer import Organizer
from app.services.mover import Mover


organize_bp = Blueprint(
    "organize",
    __name__
)


@organize_bp.route("/organize", methods=["POST"])
def organize():

    folder = request.form.get("folder", "").strip()

    if not folder:
        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message="⚠️ Silakan pilih folder terlebih dahulu."
        )

    scanner = Scanner(folder)

    if not scanner.folder_path.exists():
        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message="⚠️ Folder tidak ditemukan."
        )

    if not scanner.folder_path.is_dir():
        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message="⚠️ Lokasi yang dimasukkan bukan sebuah folder."
        )

    try:
        files = sorted(
            scanner.scan(),
            key=lambda file: file.name.lower()
        )
    except PermissionError:
        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message=(
                "⚠️ FilePilot tidak memiliki izin membaca folder tersebut."
            )
        )
    except OSError:
        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message="⚠️ Terjadi masalah saat membaca folder."
        )

    organizer = Organizer(folder)
    mover = Mover()

    preview_files = []
    activity_log = []
    total = 0
    skipped = 0
    total_size = 0

    stats = {
        "images": 0,
        "documents": 0,
        "music": 0,
        "videos": 0,
        "installers": 0,
        "others": 0
    }

    for file in files:

        category = organizer.get_category(
            file.name,
            file.extension
        )

        try:
            total_size += file.path.stat().st_size
        except OSError:
            pass

        if category == "Images":
            stats["images"] += 1
        elif category == "Documents" or category.startswith("Documents/"):
            stats["documents"] += 1
        elif category == "Music":
            stats["music"] += 1
        elif category == "Videos":
            stats["videos"] += 1
        elif category == "Installers":
            stats["installers"] += 1
        else:
            stats["others"] += 1

        success = mover.move(file.path, category)

        preview_files.append({
            "name": file.name,
            "extension": file.extension,
            "category": category
        })

        activity_log.append({
            "name": file.name,
            "category": category,
            "status": "success" if success else "failed"
        })

        if success:
            total += 1
        else:
            skipped += 1

    total_files = len(preview_files)

    if total_size >= 1024 ** 3:
        total_size_formatted = f"{total_size / (1024 ** 3):.2f} GB"
    elif total_size >= 1024 ** 2:
        total_size_formatted = f"{total_size / (1024 ** 2):.2f} MB"
    elif total_size >= 1024:
        total_size_formatted = f"{total_size / 1024:.2f} KB"
    else:
        total_size_formatted = f"{total_size} B"

    summary = {
        "total_files": total_files,
        "total_size": total_size_formatted
    }

    return render_template(
        "result.html",
        folder=folder,
        stats=stats,
        summary=summary,
        total=total,
        skipped=skipped,
        activity_log=activity_log
    )
