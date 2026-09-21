# 🚀 FilePilot

FilePilot adalah aplikasi web berbasis Flask yang digunakan untuk mengorganisir file secara otomatis berdasarkan jenis dan format file.

## ✨ Fitur

- 📁 Preview isi folder sebelum file diorganisir
- 🗂️ Mengelompokkan file berdasarkan kategori
- 📄 Memisahkan file Office berdasarkan jenisnya
- 💿 Mendeteksi file installer
- 🔍 Menangani file dengan format yang tidak dikenal
- 🔤 Mengurutkan file berdasarkan nama secara A–Z
- 📊 Menampilkan statistik file
- ⚡ Loading animation saat proses organisasi
- 🛡️ Tidak menimpa file yang sudah memiliki nama sama
- 📂 Membuat folder tujuan secara otomatis

## 📂 Kategori File

| Format | Kategori |
|---|---|
| `.doc`, `.docx`, `.odt` | Documents/Word |
| `.xls`, `.xlsx`, `.ods` | Documents/Excel |
| `.ppt`, `.pptx`, `.odp` | Documents/PowerPoint |
| `.pdf` | Documents/PDF |
| `.jpg`, `.jpeg`, `.png`, `.gif` | Images |
| `.mp3`, `.wav`, `.flac` | Music |
| `.mp4`, `.mkv`, `.avi` | Videos |
| `.exe`, `.msi`, `.msix`, `.appx` | Installers |
| `.zip`, `.rar`, `.7z` | Archives |
| Format lainnya | Others |

## 🧠 Cara Kerja

FilePilot bekerja melalui beberapa tahap:

1. Pengguna memasukkan lokasi folder.
2. FilePilot melakukan scanning terhadap file.
3. Setiap file diperiksa berdasarkan extension.
4. File dikategorikan sesuai konfigurasi.
5. Folder tujuan dibuat secara otomatis jika belum tersedia.
6. File dipindahkan ke folder yang sesuai.
7. Statistik hasil organisasi ditampilkan kepada pengguna.

## 🛠️ Teknologi

- Python
- Flask
- HTML
- CSS
- JavaScript
- Bootstrap
- python-dotenv
- JSON

## 📁 Struktur Project

```text
FILE_PILOT/
├── app/
│   ├── core/
│   ├── models/
│   ├── routes/
│   └── services/
│
├── config/
│   ├── file_types.json
│   └── office_types.json
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```
