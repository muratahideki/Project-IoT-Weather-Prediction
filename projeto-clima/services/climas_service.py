import math
from repository import obter_media_movel

def calcular_probabilidade_chuva(temp, umid, pressao, vento):
    # --- NOVOS PESOS (Atualizado) ---
    w_temp = -0.06074339
    w_umid = 0.10755981
    w_press = 0.00317959
    w_vento = 0.26779365  # Novo peso do vento
    vies = -10.9634014    # Novo viés

    # Equação Linear com 4 variáveis
    z = (w_temp * temp) + (w_umid * umid) + (w_press * pressao) + (w_vento * vento) + vies

    try:
        probabilidade = 1 / (1 + math.exp(-z))
    except OverflowError:
        probabilidade = 0 if z < 0 else 1 

    return probabilidade * 100 
