import json
from difflib import SequenceMatcher
from pathlib import Path
import re


class Organizer:

    def __init__(self, folder_path=None):
        self.folder_path = (
            Path(folder_path)
            if folder_path
            else None
        )

        self.categories = self.load_categories()
        self.office_types = self.load_office_types()

    def load_categories(self):
        config_path = Path("config/file_types.json")

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def load_office_types(self):
        config_path = Path("config/office_types.json")

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def get_office_type(self, extension):
        extension = extension.lower()

        for office, extensions in self.office_types.items():
            if extension in extensions:
                return office

        return None

    def find_matching_folder(self, file_name):
        if not self.folder_path:
            return None

        file_name_lower = file_name.lower()

        try:
            folders = [
                item
                for item in self.folder_path.iterdir()
                if item.is_dir()
            ]
        except OSError:
            return None

        for folder in folders:
            folder_name = folder.name.lower()

            if folder_name in file_name_lower:
                return folder.name

        return None

    def is_similar_word(self, text, target, threshold=0.75):
        """
        Mengecek apakah sebuah kata cukup mirip dengan kata target.

        Contoh:
        rapot ≈ rapor
        rapr  ≈ rapor
        lapran ≈ laporan
        """

        similarity = SequenceMatcher(
            None,
            text,
            target
        ).ratio()

        return similarity >= threshold

    def detect_document_type(self, keyword):

        keyword = keyword.lower()

        rapor_keywords = [
        "rapor",
        "rapot",
        "rapr",
        "rpor",
        "rapo"
    ]


        laporan_keywords = [
        "laporan",
        "lapran",
        "lporan",
        "laporn",
        "lapora"
    ]

        if keyword == "cv":
            return "CV"

        if keyword in rapor_keywords:
            return "Rapor"

        if keyword in laporan_keywords:
            return "Laporan"

        if self.is_similar_word(keyword, "rapor"):
            return "Rapor"

        if self.is_similar_word(keyword, "laporan"):
            return "Laporan"

        return None

        
        

    def get_smart_word_category(self, file_name, extension):
        """
        Mengatur file Word berdasarkan jenis dokumen dan
        huruf awal nama siswa.

        Contoh:

        rapor_andi.docx
            -> Documents/Word/Rapor/A

        rapot_bimo.docx
            -> Documents/Word/Rapor/B

        lapran_caca.docx
            -> Documents/Word/Laporan/C

        cv_dina.docx
            -> Documents/Word/CV/D
        """

        word_extensions = [
            ".doc",
            ".docx",
            ".odt"
        ]

        extension = extension.lower()

        if extension not in word_extensions:
            return None

        file_stem = Path(file_name).stem.lower()

        # Memisahkan kata jenis dokumen dan nama siswa
        # Contoh: rapot_andi -> rapot dan andi
        match = re.match(
            r"^([a-zA-Z]+)(?:[_\-\s]+)(.+)$",
            file_stem
        )

        if not match:
            return None

        keyword = match.group(1)
        student_name = match.group(2).strip()

        folder_name = self.detect_document_type(keyword)

        if not folder_name:
            return None

        if not student_name:
            return f"Documents/Word/{folder_name}/Unknown"

        first_character = student_name[0].upper()

        if first_character.isalpha():
            return (
                f"Documents/Word/{folder_name}/"
                f"{first_character}"
            )

        return f"Documents/Word/{folder_name}/Unknown"

    def get_category(self, file_name, extension):

        # Prioritas pertama: Word pintar dengan toleransi typo
        smart_word_category = self.get_smart_word_category(
            file_name,
            extension
        )

        if smart_word_category:
            return smart_word_category

        # Jika bukan Word pintar, gunakan kategori Office biasa
        office_type = self.get_office_type(extension)

        if office_type:
            return f"Documents/{office_type}"

        # Cek kecocokan dengan folder yang sudah ada
        matching_folder = self.find_matching_folder(file_name)

        if matching_folder:
            return matching_folder

        # Gunakan kategori berdasarkan ekstensi
        return self.categories.get(
            extension.lower(),
            "Others"
        )