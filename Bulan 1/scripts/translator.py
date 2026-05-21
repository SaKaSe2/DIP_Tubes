import os
import pandas as pd
from deep_translator import GoogleTranslator
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def translate_dataset():
    print("\n=== PROGRAM TRANSLASI OTOMATIS TWEET ===")
    
    file_name = input("Masukkan nama file CSV yang mau diterjemahkan (contoh: raw_tweet_massive.csv): ").strip()
    if not file_name:
        file_name = "raw_tweet_massive.csv"
        
    csv_path = os.path.join(BASE_DIR, 'data', 'raw', file_name)
    alt_csv_path = os.path.join(BASE_DIR, 'data', 'raw', 'tweets-data', file_name)
    
    if os.path.exists(alt_csv_path):
        import shutil
        print(f"Memindahkan file dari folder sementara tweets-data ke raw...")
        shutil.move(alt_csv_path, csv_path)
    
    if not os.path.exists(csv_path):
        print(f"File {csv_path} tidak ditemukan.")
        return

    print(f"Membaca dataset mentah dari: {csv_path}")
    df = pd.read_csv(csv_path)
    
    if "full_text" not in df.columns:
        print("Kolom 'full_text' tidak ditemukan. Pastikan format datanya benar.")
        return

    translator = GoogleTranslator(source='auto', target='id')
    
    print(f"\nMenerjemahkan {len(df)} baris ke Bahasa Indonesia secara otomatis...")
    print("Mohon tunggu, proses ini akan memakan waktu untuk menembus Google API...")
    
    # Membackup teks asli (Bahasa Korea/Inggris/Campur) di dalam dataset
    # Langkah ini bagus untuk dokumentasi bahwa kita menerjemahkan data asing
    if "teks_asli (original)" not in df.columns:
        df["teks_asli (original)"] = df["full_text"]
    
    total_rows = len(df)
    
    for index, row in df.iterrows():
        text = str(row["teks_asli (original)"])
        if text.strip() and text.lower() != 'nan':
            try:
                translated = translator.translate(text)
                df.at[index, "full_text"] = translated
            except Exception as e:
                # Menghindari blokir rate limit / Error Network
                time.sleep(2)
                try:
                    df.at[index, "full_text"] = translator.translate(text)
                except:
                    print(f"Gagal translate baris {index}: {text[:30]}...")
                    pass
                    
        # Update progress setiap 20 tweet
        if (index + 1) % 20 == 0 or (index + 1) == total_rows:
            print(f"  -> Progress Translasi: {index + 1} dari {total_rows} tweet selesai.")

    # Simpan kembali ke CSV supaya bisa digunakan sebagai raw data fix
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n==========================================================")
    print(f"[+] SELURUH DATA BERHASIL DITERJEMAHKAN KE BAHASA INDONESIA")
    print(f"[+] Tersimpan dan di-update langsung di: {csv_path}")
    print(f"==========================================================")

if __name__ == "__main__":
    translate_dataset()
