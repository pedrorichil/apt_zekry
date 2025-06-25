import subprocess
import socket
import os

def ping(ip):
    try:
        out = subprocess.check_output(f"ping -n 1 -w 100 {ip}", shell=True)
        return "TTL=" in out.decode(errors='ignore')
    except:
        return False

def porta_aberta(ip, porta=445):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, porta))
        s.close()
        return True
    except:
        return False

def scan_rede(prefixo="192.168.1."):
    ativos = []
    for i in range(1, 255):
        ip = f"{prefixo}{i}"
        if ping(ip) and porta_aberta(ip, 445):
            ativos.append(ip)
    return ativos

def testar_credenciais(ip, usuario, senha):
    try:
        comando = f'net use \\\\{ip}\\C$ /user:{usuario} {senha}'
        resultado = subprocess.getoutput(comando)
        if "comando concluído com êxito" in resultado.lower():
            subprocess.getoutput(f'net use \\\\{ip} /delete')  # limpa conexão
            return True
    except:
        pass
    return False

def exec_remoto(ip, usuario, senha, comando="whoami"):
    if not testar_credenciais(ip, usuario, senha):
        return f"[x] Falha na autenticação com {ip}"

    # 1. Tenta via PsExec
    try:
        ps = f'psexec \\\\{ip} -u {usuario} -p {senha} cmd /c {comando}'
        out = subprocess.getoutput(ps)
        if "não é reconhecido" not in out.lower():
            return f"[✓] Resultado via PsExec:\n{out}"
    except Exception as e:
        pass

    # 2. Fallback para WMIC
    try:
        wm = f'wmic /node:{ip} /user:{usuario} /password:{senha} process call create "cmd /c {comando}"'
        out = subprocess.getoutput(wm)
        return f"[✓] Resultado via WMIC:\n{out}"
    except Exception as e:
        return f"[x] Erro WMIC: {e}"

    return "[x] Todos métodos falharam."
