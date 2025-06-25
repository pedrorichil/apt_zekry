import platform, os
def esta_em_vm():
    sinais = ["VBOX", "VMware", "Virtual", "Sandbox"]
    nome_host = platform.node().upper()
    for s in sinais:
        if s in nome_host: return True
    return False