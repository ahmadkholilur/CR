import requests
import time
import random
import os

def isi_session():
    session = input("Masukkan sessionid (cookie) akun Indodax: ").strip()
    with open("cookie.txt", "w") as f:
        f.write(session)
    print("\033[93m\n\nSession berhasil disimpan ke cookie.txt\n\033[0m")

def isi_user_agent():
    user_agent = input("Masukkan User-Agent browser kamu: ").strip()
    with open("useragent.txt", "w", encoding="utf-8") as f:
        f.write(user_agent)
    print("\033[93m\n\nUser-Agent berhasil disimpan ke useragent.txt\n\033[0m")

def run_bot():
    if not os.path.exists("cookie.txt"):
        print("\n[PERINGATAN] File cookie.txt belum ada. Silakan isi session dulu lewat menu 1.\n")
        return
    if not os.path.exists("useragent.txt"):
        print("\n[PERINGATAN] File useragent.txt belum ada. Silakan isi User-Agent dulu lewat menu 2.\n")
        return

    with open("cookie.txt", "r") as f:
        cookie_value = f.read().strip()
    with open("useragent.txt", "r", encoding="utf-8") as f:
        user_agent = f.read().strip()

    kata_kunci = input("Masukkan nama koin (misal: BTC, ETH, DOGE): ")
    waktu_jeda = float(input("Masukkan waktu jeda antar pesan (dalam detik): "))

    url = "https://indodax.com/api/v2/chatroom/web/send_message"
    headers = {
        "Cookie": cookie_value,
        "User-Agent": user_agent
    }
    room_id = 1

    with open("pesan.txt", "r", encoding="utf-8") as file:
        pesan_template = [line.strip() for line in file if line.strip()]

    random.shuffle(pesan_template)
    berhasil_count = 0 
    for template in pesan_template:
        pesan = template.format(koin=kata_kunci)
        data = {
            "room_id": room_id,
            "message": pesan
        }
        response = requests.post(url, headers=headers, data=data)
        try:
            hasil = response.json()
            if hasil.get("success") == True:
                berhasil_count += 1
                print(f"\033[92m[BERHASIL] {berhasil_count} : {pesan}\033[0m")
            else:
                print("\033[91mGagal! Perbaharui COOKIE\033[0m")
        except:
            print("\033[91mGagal! Check kembali bagian COOKIE atau USER-AGENT \033[0m")
        time.sleep(waktu_jeda)

def main():
    while True:
        print("\033[94m\n*** MENU BOT CHATROOM INDODAX ***\033[0m")
        print("1. Isi Cookie (perbaharui jika kadaluarsa)")
        print("2. Isi User-Agent (jika sudah abaikan)")
        print("3. Run bot")
        print("4. Keluar")
        pilihan = input("Pilih menu (1/2/3/4): ").strip()

        if pilihan == "1":
            isi_session()
        elif pilihan == "2":
            isi_user_agent()
        elif pilihan == "3":
            run_bot()
        elif pilihan == "4":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 1, 2, 3, atau 4.")

if __name__ == "__main__":
    main()