import subprocess
def exec_remoto(ip, usuario, senha):
    try:
        comando = f'psexec \\\\{ip} -u {usuario} -p {senha} cmd /c whoami'
        return subprocess.getoutput(comando)
    except Exception as e:
        return str(e)

def scan_rede(prefixo="192.168.1."):
    ativos = []
    for i in range(1, 20):
        ip = f"{prefixo}{i}"
        if subprocess.call(f"ping -n 1 -w 100 {ip} >nul", shell=True) == 0:
            ativos.append(ip)
    return ativos