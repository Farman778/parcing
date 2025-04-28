import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Axtarış linki (nümunə link - burada konkret velosiped bölməsi olmalıdır)
url = "https://tap.az/elanlar/nəqliyyat/velosipedler"

# Sayta insan kimi sorğu atmaq üçün header əlavə edirik
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Sorğunu göndəririk
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

# HTML-i parse edirik
soup = BeautifulSoup(response.text, 'html.parser')

# Elanları tapırıq
elanlar = soup.find_all('div', class_='products-i')

# Excel faylı üçün kitab və səhifə yaradırıq
wb = Workbook()
ws = wb.active
ws.title = "Velosipedler"

# Sütun başlıqları
ws.append(["Ad", "Qiymət (AZN)", "Link"])

# Qiymət aralığı
minimum_qiymet = 200
maksimum_qiymet = 350

for elan in elanlar:
    try:
        ad = elan.find('div', class_='products-i-title').text.strip()
        qiymet_text = elan.find('div', class_='products-i-price').text.strip()
        qiymet_text = qiymet_text.replace("AZN", "").replace(" ", "")
        link = "https://tap.az" + elan.find('a', href=True)['href']

        qiymet = int(qiymet_text)

        if minimum_qiymet <= qiymet <= maksimum_qiymet:
            # Excel faylına yazırıq
            ws.append([ad, qiymet, link])

    except Exception as e:
        # Problem olsa keçir
        continue

# Excel faylını saxlayırıq
wb.save("velosipedler.xlsx")

print("200-350 AZN arası velosipedlər 'velosipedler.xlsx' faylına yazıldı!")
