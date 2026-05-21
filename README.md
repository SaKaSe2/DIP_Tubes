# 🚀 Dokumentasi Pipeline Data Tubes DIP

Halo! Repository ini isinya *source code* dan dokumentasi buat Tugas Besar (Tubes) mata kuliah Data Informasi Pengetahuan (DIP). Intinya, di sini kita bikin *pipeline* otomatis buat ngebersihin data teks dari Twitter/X. Data mentah yang awalnya kotor, penuh *typo*, dan bahasa gaul bakal disulap jadi data yang rapi dan siap buat dianalisis (khususnya buat analisis teks keluhan kesehatan mental).

---

## 📂 Struktur Folder
Semua *magic*-nya ada di dalam folder `Bulan 2` dan `Bulan 3`:
- **Bulan 2**: Fokus ke *Cleaning* dan normalisasi bahasa gaul (slang).
- **Bulan 3**: Fokus ke pemberian label secara spesifik (*Domain-Specific Labeling*) dan validasi.

---

## 🛠️ Penjelasan Fungsi Kodingan (Teknis)

Di dalam file-file Jupyter Notebook (`.ipynb`) dan skrip Python yang udah dibikin, ada beberapa fungsi utama yang kita pake buat ngolah data:

### 1. Fungsi `basic_cleaning(text)`
*Lokasi: Pipeline Preprocessing Bulan 2*

Fungsi ini tuh ibarat sapu ijuk buat ngebersihin kotoran-kotoran yang jelas keliatan di data teks (Twitter).
- **Ngapain aja dia?**
  - **Case Folding**: Ngecilin semua huruf pake `.lower()` biar seragam (nggak pusing bedain "Aku" sama "aku").
  - **Regex Cleaning**: Pake *library* `re` (Regular Expression) buat ngehapus hal-hal yang ga penting buat analisis:
    - `re.sub(r'http\S+|www\.\S+', '', text)` ➔ Buat ngebuang link URL.
    - `re.sub(r'#\w+', '', text)` ➔ Buat ngilangin hashtag.
    - `re.sub(r'@\w+', '', text)` ➔ Buat ngilangin mention orang.
    - `re.sub(r'\d+', '', text)` ➔ Buat ngehapus angka-angka.
    - Ngebuang tanda baca dan spasi yang kelebihan biar teksnya mulus.

### 2. Fungsi `normalize_slang(text, dictionary)`
*Lokasi: Pipeline Preprocessing Bulan 2*

Nah, fungsi ini krusial banget buat ngubah bahasa "alay" atau gaul jadi bahasa formal baku.
- **Gimana cara kerjanya?** 
  - Pertama, kita siapin dulu `slang_dict` (kamus slang) yang isinya *mapping* kata. Contoh: `'bgt': 'sekali', 'aq': 'saya'`.
  - Terus, fungsi ini bakal mecah kalimat per kata pake `text.split()`.
  - Abis itu, dia ngecek satu-satu pake *list comprehension*: `[dictionary.get(word, word) for word in words]`. Kalau katanya ada di kamus, diganti sama versi bakunya. Kalo nggak ada, ya dibiarin aja aslinya.
  - Tujuannya buat ngejaga **Data Integrity**, maknanya tetep sama walau bahasanya dirapihin.

### 3. Proses Filtering (Menghapus Data Noise)
Ini bukan fungsi terpisah sih, tapi pake fitur `.apply` dari Pandas.
- Kita ngitung jumlah kata ditiap baris data. Kalo misalnya tweet-nya kurang dari 3 kata (contoh: cuma ngetik "wkwk"), datanya langsung didrop/dibuang karena dianggap *noise* atau nggak relevan buat dianalisis.

### 4. Fungsi `apply_keyword_labeling(text)`
*Lokasi: Domain Specific Labeling Bulan 3*

Setelah datanya bersih dan baku, kita perlu ngasih label (kategori) biar ada konteksnya. Di sini pake pendekatan *Keyword-based Labeling*.
- **Cara kerjanya**:
  - Kita udah *define* rules (aturan) berupa keyword buat masing-masing kelas. Misalnya buat kategori "Insomnia", keywordnya `['tidur', 'lelah', 'begadang']`.
  - Fungsi ini bakal nge-loop semua kategori. Kalau teksnya mengandung salah satu keyword tersebut (pake kondisi `if keyword in text:`), data itu otomatis dikasih label kategori tersebut.
  - Kalau sampe akhir nggak nemu satupun keyword yang cocok, yaudah masuknya ke label `Lainnya / Netral`.

---

## ✅ Tahap Validasi Manual (Minggu 11-12)
Buat mastiin kodingan kita kerjanya bener, kita juga bikin script `Validation.ipynb` buat narik **100 sampel baris acak**. Sampel ini nanti bakal di-ekspor ke Excel `sample_validasi_manual.xlsx` lengkap dengan kolom kosong buat dicek manual secara teliti sama kita. Tujuannya buat ngevaluasi seberapa akurat hasil dari fungsi-fungsi di atas.

---
*Dibuat untuk memenuhi Tugas Besar Data Informasi Pengetahuan C.*
