 import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.obilet.com/seferler/409-678/2026-03-13"
DOSYA = "firmalar.json"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

def onceki_firmalari_oku():
    if not os.path.exists(DOSYA):
        return []
    with open(DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)

def firmalari_kaydet(firma_listesi):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(firma_listesi, f, ensure_ascii=False)

def check_ticket():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(10)  # sayfanın yüklenmesi için bekle

    # Görünür firma elementlerini çekiyoruz
    firma_elements = driver.find_elements(By.CSS_SELECTOR, "div.seferFirmasi")  # örnek selector
    firma_listesi = [e.text.strip().lower() for e in firma_elements if e.text.strip()]

    driver.quit()

    if not firma_listesi:
        print("Firma bulunamadı.")
        return

    onceki = onceki_firmalari_oku()
    yeni_firmalar = [f for f in firma_listesi if f not in onceki]

    if yeni_firmalar:
        mesaj = "🚨 Yeni firma eklendi:\n" + "\n".join(yeni_firmalar)
        send_message(mesaj)

    firmalari_kaydet(firma_listesi)
    print("Kontrol tamamlandı. Firma listesi kaydedildi.")

check_ticket()
