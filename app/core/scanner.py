from pathlib import Path
from app.models.file_info import FileInfo


class Scanner:

    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)

    def scan(self):
        files = []

        for item in self.folder_path.iterdir():

            if item.is_file():

                files.append(
                    FileInfo(
                        path=item,
                        name=item.name,
                        extension=item.suffix,
                        is_file=item.is_file(),
                        is_directory=item.is_dir()
                    )
                )

        return files