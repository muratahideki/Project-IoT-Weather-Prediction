# tasks.py
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import requests
import math
import atexit

# --- CONFIGURAÇÃO DA API EXTERNA (VENTO) ---
API_KEY = "2dca8a2bed77e01a0b189944dd3fda0f"  # <--- COLOQUE SUA CHAVE AQUI
LAT = "-22.73"  
LON = "-45.12"
URL_API = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# --------- Funções Auxiliares ---------

def obter_vento_externo():
    """ Vai na internet e pega o vento atual """
    try:
        response = requests.get(URL_API)
        dados = response.json()
        velocidade_vento = dados['wind']['speed'] 
        nome_cidade = dados['name']
        return velocidade_vento, nome_cidade
    except:
        return 0.0, "Erro API"

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

# --------- Robô de Automação (Calcula Médias) ---------
def calcular_media_hora_anterior():
    print(">>> Calculando média da hora anterior...")
    agora = datetime.now()
    data_fim = agora.replace(minute=0, second=0, microsecond=0)
    data_inicio = data_fim - timedelta(hours=1)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Agora calculamos AVG(vento) também
    cursor.execute("""
        SELECT AVG(temperatura), AVG(pressao), AVG(altitude), AVG(umidade), AVG(vento), COUNT(*) 
        FROM medidas WHERE data_hora >= ? AND data_hora < ?
    """, (data_inicio.isoformat(), data_fim.isoformat()))
    
    resultado = cursor.fetchone()

    if resultado and resultado[5] > 0: # resultado[5] é o Count
        cursor.execute("""
            INSERT INTO resumos (inicio_periodo, fim_periodo, media_temp, media_pressao, media_altitude, media_umidade, media_vento, qtd_amostras, data_geracao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data_inicio.isoformat(), data_fim.isoformat(), 
              resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], 
              resultado[5], agora.isoformat()))
        conn.commit()
        print(">>> Média (incluindo vento) salva no histórico.")
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=calcular_media_hora_anterior, trigger="cron", minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
