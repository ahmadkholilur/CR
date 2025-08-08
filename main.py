import requests
import time
import random
import os

def isi_session():
    session = input("Masukkan sessionid (cookie) akun Indodax: ").strip()
    with open("cookie.txt", "w") as f:
        f.write(session)
    print("\033[92m\n\nSession berhasil disimpan ke cookie.txt\n\033[0m")

def isi_user_agent():
    user_agent = input("Masukkan User-Agent browser kamu: ").strip()
    with open("useragent.txt", "w", encoding="utf-8") as f:
        f.write(user_agent)
    print("\033[92m\n\nUser-Agent berhasil disimpan ke useragent.txt\n\033[0m")

def get_last_index():
    if os.path.exists("last_index.txt"):
        with open("last_index.txt", "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def save_last_index(idx):
    with open("last_index.txt", "w") as f:
        f.write(str(idx))

def run_bot():
    if not os.path.exists("cookie.txt"):
        print("\033[93m\n[PERINGATAN] File cookie.txt belum ada. \nSilakan isi session dulu lewat menu 1.\n\033[0m")
        return
    if not os.path.exists("useragent.txt"):
        print("\033[93m\n[PERINGATAN] File useragent.txt belum ada. \nSilakan isi User-Agent dulu lewat menu 2.\n\033[0m")
        return

    with open("cookie.txt", "r") as f:
        cookie_value = f.read().strip()
    with open("useragent.txt", "r", encoding="utf-8") as f:
        user_agent = f.read().strip()

    kata_kunci = input("Masukkan nama koin (misal: BTC, ETH, DOGE): ")

    # Input jeda minimal dan maksimal dari user
    while True:
        try:
            jeda_min = float(input("Masukkan jeda minimal antar pesan (detik): "))
            jeda_max = float(input("Masukkan jeda maksimal antar pesan (detik): "))
            if jeda_min > jeda_max:
                print("Jeda minimal tidak boleh lebih besar dari jeda maksimal!")
                continue
            break
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")

    url = "https://indodax.com/api/v2/chatroom/web/send_message"
    headers = {
        "Cookie": cookie_value,
        "User-Agent": user_agent,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://indodax.com",
        "Referer": "https://indodax.com/market/BTCIDR",
        "X-Requested-With": "XMLHttpRequest"
    }
    room_id = 1

    try:
        with open("pesan.txt", "r", encoding="utf-8") as file:
            pesan_template = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("\033[91mFile pesan.txt tidak ditemukan!\033[0m")
        return

    berhasil_count = 0 
    gagal_total = 0  # Counter total gagal

    last_index = get_last_index()
    print(f"\033[93mMulai dari baris ke-{last_index+1} pada pesan.txt\033[0m")

    for idx, template in enumerate(pesan_template[last_index:], start=last_index):
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
                gagal_total += 1
                print(f"\033[91mGagal! Perbaharui COOKIE (Total gagal: {gagal_total}{pesan})\033[0m")
        except:
            gagal_total += 1
            print(f"\033[91mGagal! Check kembali bagian COOKIE atau USER-AGENT (Total gagal: {gagal_total})\033[0m")
        
        save_last_index(idx + 1)  # Simpan index terakhir yang sudah dikirim

        if gagal_total >= 4:
            print("\033[91mTotal gagal sudah 4x, program dihentikan otomatis!\033[0m")
            break

        jeda = random.uniform(jeda_min, jeda_max)
        # print(f"Menunggu {jeda:.2f} detik sebelum mengirim pesan berikutnya...")
        time.sleep(jeda)

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
