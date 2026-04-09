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
ultimo_update = None

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def verificar_comandos():
    global ultimo_update
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        r = requests.get(url).json()

        for item in r["result"]:
            update_id = item["update_id"]

            if ultimo_update is None or update_id > ultimo_update:
                ultimo_update = update_id

                if "message" in item:
                    text = item["message"].get("text", "")
                    chat_id = item["message"]["chat"]["id"]

                    if text == "/start" and str(chat_id) == CHAT_ID:
                        enviar_telegram("🟢 Bot online e monitorando ingressos!")
    except:
        pass


headers = {"User-Agent": "Mozilla/5.0"}

def verificar():
    for data, slug in EVENTOS.items():
        try:
            url = f"https://www.ticketmaster.com.br/api/quick-picks/{slug}"
            r = requests.get(url, headers=headers)

            disponivel = False
            if r.status_code == 200:
                data_json = r.json()
                if "picks" in data_json and len(data_json["picks"]) > 0:
                    disponivel = True

            if disponivel and not estado[data]:
                enviar_telegram(
                    f"🚨 INGRESSOS DISPONÍVEIS BTS {data}!\n"
                    f"https://www.ticketmaster.com.br/event/{slug}"
                )
                estado[data] = True

            if not disponivel:
                estado[data] = False

        except:
            pass

enviar_telegram("🤖 Bot BTS online e monitorando ingressos!")

while True:
    verificar_comandos()
    verificar()
    time.sleep(10)
