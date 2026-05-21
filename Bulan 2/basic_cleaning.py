import os
import re
import pandas as pd

# Konfigurasi Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Folder Tubes
INPUT_FILE = os.path.join(BASE_DIR, 'Gabungan.xlsx')
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__)) # Folder Bulan 2
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'dataset_cleaned.xlsx')

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # 1. Case folding (mengecilkan huruf)
    text = text.lower()
    
    # 2. Regex cleaning
    # Hapus URL
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Hapus hashtag
    text = re.sub(r'#\w+', '', text)
    # Hapus mention (umum pada tweet)
    text = re.sub(r'@\w+', '', text)
    # Hapus angka
    text = re.sub(r'\d+', '', text)
    
    # Hapus tanda baca/karakter spesial dan spasi ekstra
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def run_pipeline():
    print("=== PROGRAM BASIC CLEANING TWEETS ===")
    print(f"[*] Membaca dataset dari: {INPUT_FILE}")
    try:
        df = pd.read_excel(INPUT_FILE)
    except Exception as e:
        print(f"[-] Error membaca file: {e}")
        return

    if 'full_text' not in df.columns:
        print("[-] Kolom 'full_text' tidak ditemukan dalam dataset.")
        return

    print(f"[+] Jumlah data awal: {len(df)} baris")
    
    # Proses Cleaning
    print("\n[*] Memulai proses Basic Cleaning (Case folding & Regex)...")
    df['cleaned_text'] = df['full_text'].apply(clean_text)
    
    # 3. Filtering (menghapus tweet yang terlalu pendek atau tidak relevan)
    print("[*] Memulai proses Filtering (Menghapus tweet < 3 kata)...")
    # Hitung jumlah kata
    df['word_count'] = df['cleaned_text'].apply(lambda x: len(str(x).split()))
    
    # Menyaring data dengan minimal 3 kata
    df_filtered = df[df['word_count'] >= 3].copy()
    
    # Drop kolom bantu word_count agar lebih bersih
    df_filtered = df_filtered.drop(columns=['word_count'])
    
    print(f"[+] Jumlah data setelah filtering: {len(df_filtered)} baris")
    print(f"[-] Data noise/pendek yang dihapus: {len(df) - len(df_filtered)} baris")
    
    # Menyimpan hasil
    print(f"\n[*] Menyimpan hasil dataset bersih ke: {OUTPUT_FILE}")
    df_filtered.to_excel(OUTPUT_FILE, index=False)
    print("[+] ALHAMDULILLAH SELESAI! Pipeline preprocessing tahap 1 berhasil.")

if __name__ == "__main__":
    run_pipeline()
