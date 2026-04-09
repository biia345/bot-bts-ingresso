import requests
import time

TOKEN = "8769429050:AAHNSzlsX-zjygI8K4gM6d8eqZ72-tQwdW8"
CHAT_ID = "-1003838454435"

EVENTOS = {
    "28/10": "pre-venda-army-membership-bts-world-tour-arirang-28-10",
    "30/10": "pre-venda-army-membership-bts-world-tour-arirang-30-10",
    "31/10": "pre-venda-army-membership-bts-world-tour-arirang-31-10"
}

estado = {data: False for data in EVENTOS}

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

enviar_telegram("🤖 Bot BTS online e monitorando ingressos!")

def verificar():
    for data, slug in EVENTOS.items():
        try:
            url = f"https://www.ticketmaster.com.br/api/quick-picks/{slug}"
            r = requests.get(url, headers=headers, timeout=10)

            if r.status_code != 200:
                continue

            data_json = r.json()

            disponivel = False

            # verifica se existe inventário disponível
            if "picks" in data_json:
                if len(data_json["picks"]) > 0:
                    disponivel = True

            if disponivel and not estado[data]:
                enviar_telegram(
                    f"🚨 INGRESSOS DISPONÍVEIS BTS {data}!\n"
                    f"https://www.ticketmaster.com.br/event/{slug}"
                )
                estado[data] = True

            if not disponivel:
                estado[data] = False

        except Exception as e:
            print("Erro:", e)

while True:
    verificar()
    time.sleep(10)
