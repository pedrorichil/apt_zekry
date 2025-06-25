import time
def ativar_apenas_apos(hora="09"):
    atual = time.strftime("%H")
    return int(atual) >= int(hora)