import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

URL = "https://www.obilet.com/seferler/409-678/2026-03-13"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

def check_ticket():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(8)

    page_source = driver.page_source

    if "Sefer Bulunamadı" not in page_source and "Sefer bulunamadı" not in page_source:
        send_message("🚍 Şanlıurfa → Salihli için 13 Mart 2026 sefer görünüyor!")

    driver.quit()

while True:
    check_ticket()
    time.sleep(600)
