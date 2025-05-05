import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time
from datetime import datetime

# Telegram bot token və chat ID
BOT_TOKEN = ""
CHAT_ID =""

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    return response

def scrape_and_send():
    url = "https://tap.az/elanlar/nəqliyyat/velosipedler"
    headers = {
        "User-Agent": "Mozilla/5.0 ..."
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    elanlar = soup.find_all('div', class_='products-i')

    wb = Workbook()
    ws = wb.active
    ws.title = "Velosipedler"
    ws.append(["Ad", "Qiymət (AZN)", "Link"])

    minimum_qiymet = 200
    maksimum_qiymet = 350

    for elan in elanlar:
        try:
            ad = elan.find('div', class_='products-i-title').text.strip()
            qiymet_text = elan.find('div', class_='products-i-price').text.strip()
            qiymet_text = qiymet_text.replace("AZN", "").replace(" ", "").replace(",", ".")
            qiymet = float(qiymet_text)
            link = "https://tap.az" + elan.find('a', href=True)['href']

            if minimum_qiymet <= qiymet <= maksimum_qiymet:
                ws.append([ad, qiymet, link])
                mesaj = f"<b>{ad}</b>\nQiymət: {qiymet} AZN\nLink: {link}"
                send_telegram_message(mesaj)

        except Exception as e:
            print(f"Xəta baş verdi: {e}")
            continue

    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"velosipedler_{now}.xlsx"
    wb.save(filename)
    print(f"{now} - Fayl saxlandı və elanlar Telegrama göndərildi.")

# Sonsuz dövr - hər 12 saatdan bir işləyəcək
while True:
    scrape_and_send()
    print("12 saat gözlənilir...")
    time.sleep(43200)  # 12 saat = 43200 saniyə
