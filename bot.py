import requests
import time

TOKEN = "8769429050:AAHNSzlsX-zjygI8K4gM6d8eqZ72-tQwdW8"
CHAT_ID = "1788006532"

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

headers = {
    "User-Agent": "Mozilla/5.0"
}

enviar_telegram("🤖 Bot BTS online e monitorando ingressos!")

def verificar():
    for data, url in URLS.items():
        try:
            r = requests.get(url, headers=headers, timeout=10)
            page = r.text

            disponivel = (
                "Disponível" in page or
                "Available" in page or
                "Comprar" in page or
                "Buy" in page
            )

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
