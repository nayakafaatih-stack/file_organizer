from flask import Blueprint, request, render_template

from app.core.scanner import Scanner
from app.services.organizer import Organizer


preview_bp = Blueprint(
    "preview",
    __name__
)


@preview_bp.route("/preview", methods=["POST"])
def preview():

    # ===========================
    # Ambil Folder
    # ===========================

    folder = request.form.get(
        "folder",
        ""
    ).strip()

    # ===========================
    # Validasi Input
    # ===========================

    if not folder:

        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message="⚠️ Silakan pilih folder terlebih dahulu."
        )

    # ===========================
    # Scanner
    # ===========================

    scanner = Scanner(folder)

    # ===========================
    # Validasi Folder
    # ===========================

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

    # ===========================
    # Scan Files
    # ===========================

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
                "⚠️ FilePilot tidak memiliki "
                "izin membaca folder tersebut."
            )
        )

    except OSError:

        return render_template(
            "index.html",
            files=[],
            folder=folder,
            error_message=(
                "⚠️ Terjadi masalah saat "
                "membaca folder."
            )
        )

    # ===========================
    # Smart Organizer
    # ===========================

    organizer = Organizer(folder)

    preview_files = []

    # ===========================
    # Statistics
    # ===========================

    stats = {

        "images": 0,
        "documents": 0,
        "music": 0,
        "videos": 0,
        "installers": 0,
        "others": 0

    }

    # ===========================
    # Process Files
    # ===========================

    for file in files:

        # Lewati folder
        if not file.is_file:
            continue

        # ===========================
        # Smart Category
        # ===========================

        category = organizer.get_category(

            file.name,

            file.extension

        )

        # ===========================
        # Preview Data
        # ===========================

        preview_files.append({

            "name": file.name,

            "extension": file.extension,

            "category": category

        })

        # ===========================
        # Statistics
        # ===========================

        if category == "Images":

            stats["images"] += 1

        elif category == "Documents":

            stats["documents"] += 1

        elif category == "Music":

            stats["music"] += 1

        elif category == "Videos":

            stats["videos"] += 1

        elif category == "Installers":
            
            stats["installers"] += 1

        else:

            stats["others"] += 1

    # ===========================
    # Render
    # ===========================

    return render_template(

        "index.html",

        files=preview_files,

        folder=folder,

        stats=stats

    )