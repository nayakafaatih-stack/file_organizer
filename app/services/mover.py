import shutil
from pathlib import Path


class Mover:

    def move(self, source: Path, category: str) -> bool:

        if not source.exists():
            return False

        destination_folder = (
            source.parent / category
        )

        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            destination_folder / source.name
        )

        if destination.exists():
            return False

        try:

            shutil.move(
                source,
                destination
            )

            return True

        except Exception:

            return False