import yt_dlp
import os
import random
import re

BASE_PATH = "/sdcard/XelDL"

ua_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

def banner():
    os.system("clear")
    print("""
╔══════════════════════════════════╗
║        XelAllDownloader 😈       ║
╚══════════════════════════════════╝

[1] HD Video
[2] MP3
[3] Ganti Folder
[4] Info

STOP / EXIT / Q = keluar
""")

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%')
        print(f"\r📥 Downloading... {percent}", end="")
    elif d['status'] == 'finished':
        print("\n🔄 Processing...")

current_path = BASE_PATH
os.makedirs(current_path, exist_ok=True)

while True:
    banner()
    print(f"📂 Folder: {current_path}\n")

    pilih = input("Pilih: ").strip().lower()

    if pilih in ["stop", "exit", "q"]:
        print("👋 Bye!")
        break

    # GANTI FOLDER
    if pilih == "3":
        new_path = input("\nFolder baru: ").strip()

        if new_path:
            if not os.path.exists(new_path):
                print("1. Buat folder\n2. Batal")
                p = input("> ")
                if p == "1":
                    os.makedirs(new_path)
                    current_path = new_path
                else:
                    continue
            else:
                current_path = new_path
        continue

    # INFO
    if pilih == "4":
        print("""
🔥 XelAllDownloader Ultimate
- HD & MP3
- Anti Block++
- Progress bar
- Flexible folder
""")
        input("\nENTER...")
        continue

    if pilih not in ["1", "2"]:
        continue

    url = input("\n🔗 URL: ").strip()
    if url.lower() in ["stop", "exit", "q"]:
        break

    if not url:
        continue

    nama = input("✏️ Nama file (opsional): ").strip()
    nama = clean_filename(nama)

    if nama:
        output = f"{current_path}/{nama}.%(ext)s"
    else:
        output = f"{current_path}/%(title)s.%(ext)s"

    common_opts = {
        'outtmpl': output,
        'noplaylist': True,
        'retries': 5,
        'fragment_retries': 5,
        'sleep_interval': 2,
        'max_sleep_interval': 5,
        'progress_hooks': [progress_hook],
        'http_headers': {
            'User-Agent': random.choice(ua_list),
            'Referer': 'https://www.tiktok.com/'
        }
    }

    if pilih == "1":
        common_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        })
    else:
        common_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    print("\n⚙️ Starting...\n")

    try:
        with yt_dlp.YoutubeDL(common_opts) as ydl:
            ydl.download([url])

        print("\n✅ DONE")

    except Exception as e:
        print("\n❌ ERROR:", e)

    input("\nENTER...")