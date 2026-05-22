# Dokumentasi Pipeline Data Tubes DIP

Repository ini isinya source code dan dokumentasi buat Tugas Besar (Tubes) mata kuliah Data Informasi Pengetahuan (DIP). Intinya, di sini kita bikin pipeline otomatis buat ngebersihin data teks dari Twitter/X. Data mentah yang awalnya kotor, penuh typo, dan bahasa gaul bakal disulap jadi data yang rapi dan siap buat dianalisis.

---

## Struktur Folder

```
Tubes/
├── Gabungan.xlsx                  <- Dataset utama (sumber data semua notebook)
├── README.md
├── tubes DIP.docx
├── Bulan 1/
│   ├── Data_Profiling.ipynb       <- Analisis kekotoran data
│   └── scripts/                   <- Scraper & Translator
├── Bulan 2/
│   ├── Pipeline_Preprocessing_Bulan2.ipynb  <- Cleaning + Normalisasi
│   ├── basic_cleaning.py          <- Script cleaning (bisa dirun terpisah)
│   └── dataset_cleaned.xlsx       <- Output cleaning
└── Bulan 3/
    ├── Domain_Specific_Labeling.ipynb  <- Keyword-based Labeling
    ├── Validation.ipynb                <- Validasi manual 100 sampel
    └── dataset_labeled_bulan3.xlsx     <- Output labeling
```

**Alur data:** `Gabungan.xlsx` -> Bulan 1 (Profiling) -> Bulan 2 (Cleaning) -> Bulan 3 (Labeling & Validasi)

Semua notebook baca dari `Gabungan.xlsx` atau output bulan sebelumnya. Jadi kalo datanya nambah, tinggal update `Gabungan.xlsx` terus re-run notebook dari Bulan 1 ke bawah tanpa perlu ubah kode.

---

## Penjelasan Fungsi Kodingan (Teknis)

### 1. Fungsi `basic_cleaning(text)`
*Lokasi: Pipeline Preprocessing Bulan 2*

Fungsi ini buat ngebersihin kotoran-kotoran yang keliatan di data teks Twitter.
- **Case Folding**: Ngecilin semua huruf pake `.lower()` biar seragam.
- **Regex Cleaning**: Pake library `re` buat ngehapus:
  - Link URL (`http...`, `www...`)
  - Hashtag (`#...`)
  - Mention (`@...`)
  - Angka-angka
  - Tanda baca dan spasi berlebih

### 2. Fungsi `normalize_slang(text, dictionary)`
*Lokasi: Pipeline Preprocessing Bulan 2*

Fungsi ini buat ngubah bahasa gaul/singkatan jadi bahasa formal baku.
- Kita siapin dulu `slang_dict` yang isinya mapping kata. Contoh: `'bgt': 'sekali'`, `'aq': 'saya'`.
- Fungsi ini mecah kalimat per kata pake `text.split()`, terus ngecek satu-satu di kamus. Kalo katanya ada di kamus ya diganti, kalo nggak ya dibiarin.
- Tujuannya buat ngejaga Data Integrity, maknanya tetep sama walau bahasanya dirapihin.

### 3. Proses Filtering
Kita ngitung jumlah kata di tiap baris data. Kalo tweet-nya kurang dari 3 kata, datanya langsung dibuang karena dianggap noise atau nggak relevan.

### 4. Fungsi `apply_keyword_labeling(text)`
*Lokasi: Domain Specific Labeling Bulan 3*

Setelah datanya bersih dan baku, kita ngasih label (kategori) pake pendekatan Keyword-based Labeling.
- Kita udah define rules berupa keyword buat masing-masing kelas. Misalnya buat "Insomnia", keywordnya `['tidur', 'lelah', 'begadang']`.
- Fungsi ini nge-loop semua kategori. Kalo teksnya mengandung salah satu keyword, data itu dikasih label kategori tersebut.
- Kalo sampe akhir nggak nemu keyword yang cocok, masuknya ke label `Lainnya / Netral`.

---

## Tahap Validasi Manual (Minggu 11-12)
Buat mastiin kodingan kita kerjanya bener, kita juga bikin `Validation.ipynb` buat narik 100 sampel baris acak. Sampel ini diekspor ke Excel `sample_validasi_manual.xlsx` lengkap dengan kolom kosong buat dicek manual.

---
*Dibuat untuk memenuhi Tugas Besar Data Informasi Pengetahuan C.*
