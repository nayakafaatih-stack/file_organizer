from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileInfo:
    path: Path
    name: str
    extension: str
    is_file: bool 
    is_directory: bool
    