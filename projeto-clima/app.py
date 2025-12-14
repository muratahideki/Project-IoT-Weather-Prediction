from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import database  # Importa seu módulo
from database import DB_NAME
from datetime import datetime, timedelta
from tasks import obter_vento_externo, calcular_probabilidade_chuva
import tasks     # Importa seu módulo

app = Flask(__name__)

# Inicia Banco
database.inicializar_db()

# Inicia Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(tasks.calcular_media_hora_anterior, trigger="cron", minute=0)
scheduler.start()

# --------- Rotas do Servidor ---------

@app.route("/dados", methods=["POST"])
def receber_dados():
    dados = request.get_json()
    
    # 1. Pega os dados do ESP32
    temp = dados.get("temp")
    press = dados.get("pressao")
    alt = dados.get("altitude")
    umid = dados.get("umidade")
    
    # 2. Pega o Vento da Internet IMEDIATAMENTE para salvar junto
    vento_atual, _ = obter_vento_externo()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 3. Salva tudo junto na tabela medidas
    cursor.execute("""
        INSERT INTO medidas (temperatura, pressao, altitude, umidade, vento, data_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (temp, press, alt, umid, vento_atual, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "salvo", "vento_registrado": vento_atual})

@app.route("/api/brutos")
def api_brutos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medidas ORDER BY id DESC LIMIT 60")
    dados = cursor.fetchall()
    conn.close()
    return jsonify(dados)

@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Histórico
    cursor.execute("SELECT * FROM resumos ORDER BY id DESC")
    resumos = cursor.fetchall()

    # 2. Média Móvel dos últimos 60 minutos (Para a IA)
    uma_hora_atras = datetime.now() - timedelta(hours=1)
    
    # Calcula média de TUDO, inclusive vento
    cursor.execute("""
        SELECT AVG(temperatura), AVG(umidade), AVG(pressao), AVG(vento) 
        FROM medidas 
        WHERE data_hora >= ?
    """, (uma_hora_atras.isoformat(),))
    
    media_movel = cursor.fetchone()
    conn.close()

    # Pega nome da cidade só para exibir
    _, cidade_api = obter_vento_externo()

    # 3. Lógica da Previsão
    prob_chuva = 0
    msg_previsao = "Aguardando dados..."
    cor_card = "#eee"
    cor_texto = "#333"
    inputs_usados = [0, 0, 0, 0] # T, U, P, V

    if media_movel and media_movel[0] is not None:
        t_med, u_med, p_med, v_med = media_movel
        inputs_usados = [t_med, u_med, p_med, v_med]
        
        # Usa a nova função com 4 argumentos
        prob_chuva = calcular_probabilidade_chuva(t_med, u_med, p_med, v_med)
        
        msg_previsao = "Tendência baseada na Média (60min)"
        
        # Cores
        if prob_chuva > 50:
            cor_card = "#ffcccc"
            cor_texto = "#a00000"
            msg_previsao = "ALTA PROBABILIDADE (Tendência)"
        else:
            cor_card = "#ccffcc"
            cor_texto = "#006600"
            msg_previsao = "Baixa Probabilidade"

    return render_template(
        "dashboard.html",
        resumos=resumos,
        prob_chuva=prob_chuva,
        msg_previsao=msg_previsao,
        cor_card=cor_card,
        cor_texto=cor_texto,
        inputs_usados=inputs_usados,
        cidade=cidade_api
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
