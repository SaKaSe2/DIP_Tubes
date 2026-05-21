import os
import subprocess
import sys
import re
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DICT_DIR = os.path.join(BASE_DIR, 'dictionary')

def setup_directories():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(DICT_DIR, exist_ok=True)

def execute_scraper(auth_token, query, limit, tweet_id="umum"):
    filename = f"temp_scrape_{tweet_id}.csv"
    print(f"\n[-] Menjalankan mesin Scraper di belakang layar untuk mengambil maks {limit} tweet/komentar...")
    print(f"[*] Mengeksekusi Query Anti-Blokir: {query}")
    print(f"[-] Mohon tunggu, proses ini memakan waktu karena melakukan scrolling otomatis...\n")
    
    command = [
        "npx.cmd", "-y", "tweet-harvest@latest",
        "-o", filename,
        "-s", query,
        "-l", str(limit),
        "--token", auth_token
    ]
    
    try:
        subprocess.run(command, check=True, cwd=BASE_DIR, shell=False)
        
        temp_file = os.path.join(BASE_DIR, 'tweets-data', filename)
        master_file = os.path.join(RAW_DATA_DIR, 'raw_tweet_master_knetz.csv')
        
        if os.path.exists(temp_file):
            if os.path.exists(master_file):
                print(f"\n[+] Master Dataset ('raw_tweet_master_knetz.csv') ditemukan!")
                print(f"[+] Code menyatukan data postingan ini ke bawah data postingan sebelumnya secara otomatis...")
                import pandas as pd
                df_temp = pd.read_csv(temp_file)
                df_temp.to_csv(master_file, mode='a', header=False, index=False)
                os.remove(temp_file)
            else:
                shutil.move(temp_file, master_file)
                
            print(f"\n==============================================================")
            print(f"[+] ALHAMDULILLAH SELESAI! Komentar berhasil didownload.")
            print(f"[+] Data telah terhimpun otomatis di File : {master_file}")
            print(f"[+] Kakak bisa me-run ulang skrip ini lagi untuk postingan ke-2, ke-3 dst!")
            print(f"==============================================================")
            
            try:
                shutil.rmtree(os.path.join(BASE_DIR, 'tweets-data'))
            except:
                pass
        else:
            print("\n[-] Peringatan: Scraping selesai namun file tidak ditemukan. Mungkin X sedang membatasi.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Terjadi kesalahan teknis saat menjalankan scraper: {e}")

if __name__ == "__main__":
    print("\n=== PROGRAM SCRAPER AUTO-KOMENTAR TUGAS DATA MINING ===")
    setup_directories()

    auth_token = input("\n1. Masukkan (Paste) parameter cookie 'auth_token' Anda:\n> ").strip()
    if not auth_token:
        print("Error: 'auth_token' wajib diisi!")
        sys.exit(1)

    print("\n2. MODE TARIK KOMENTAR POSTINGAN SPESIFIK")
    print("   Karena tombol 'Share' diblokir Twitter (Visibility Limited), Kakak")
    print("   sebenarnya TETAP BISA men-copy Link postingan tersebut secara langsung")
    print("   dari ADDRESS BAR BROWSER Kakak (kolom di bagian paling atas layar Chrome).")
    print("   Contoh URL: https://x.com/umparum3/status/2023744391840465302")
    
    user_url = input("\nSilahkan PASTE Link Postingan dari Address Bar (Atau ENTER untuk pencarian umum):\n> ").strip()
    
    if user_url:
        match = re.search(r"status/(\d+)", user_url)
        if match:
            tweet_id = match.group(1)
            print(f"\n[+] Script sukses mengekstrak ID Postingan: {tweet_id}")
            query = f"conversation_id:{tweet_id}"
            pass_id = tweet_id
        else:
            print("[-] URL/Link yang dimasukkan tidak valid. Beralih ke pencarian umum otomatis.")
            query = "(knetz OR korea) (indo OR indonesia) lang:id"
            pass_id = "umum"
    else:
        print("\n[+] Beralih ke pencarian topik massif Knets vs ASEAN otomatis.")
        query = "(knetz OR korea OR 한국) (indo OR indonesia OR asean OR 인니)"
        pass_id = "umum_massive"

    user_count = input(f"\n3. Masukkan target jumlah komentar ditarik (Enter untuk default 5000):\n> ").strip()
    limit = int(user_count) if user_count.isdigit() else 5000

    execute_scraper(auth_token, query, limit, pass_id)
