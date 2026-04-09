import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

URLS = {
    "28/10": "https://www.ticketmaster.com.br/event/pre-venda-army-membership-bts-world-tour-arirang-28-10",
    "30/10": "https://www.ticketmaster.com.br/event/pre-venda-army-membership-bts-world-tour-arirang-30-10",
    "31/10": "https://www.ticketmaster.com.br/event/pre-venda-army-membership-bts-world-tour-arirang-31-10"
}

estado = {data: False for data in URLS}

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

enviar_telegram("🤖 Bot BTS online!")

def verificar():
    for data, url in URLS.items():
        try:
            driver.get(url)
            time.sleep(5)

            page = driver.page_source
            disponivel = ("Disponível" in page or "Available" in page)

            if disponivel and not estado[data]:
                enviar_telegram(f"🚨 Voltou ingresso BTS dia {data}!\n{url}")
                estado[data] = True

            if not disponivel:
                estado[data] = False

        except Exception as e:
            print("Erro:", e)

while True:
    verificar()
    time.sleep(10)
