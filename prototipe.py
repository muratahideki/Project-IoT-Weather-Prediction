from flask import Flask, request, jsonify, render_template_string, redirect
import sqlite3
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import math
import requests

app = Flask(__name__)
DB_NAME = "estacao_climatica.db"

# --- CONFIGURAÇÃO DA API EXTERNA (VENTO) ---
API_KEY = "SUA_CHAVE_AQUI"  # <--- COLOQUE SUA CHAVE AQUI
LAT = "-22.73"  
LON = "-45.12"
URL_API = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

# --------- Banco de Dados ---------
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tabela de dados brutos (Agora com VENTO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            pressao REAL,
            altitude REAL,
            umidade REAL,
            vento REAL, 
            data_hora TEXT
        )
    """)

    # 2. Tabela de Resumos (Agora com MEDIA_VENTO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inicio_periodo TEXT,
            fim_periodo TEXT,
            media_temp REAL,
            media_pressao REAL,
            media_altitude REAL,
            media_umidade REAL,
            media_vento REAL,
            qtd_amostras INTEGER,
            data_geracao TEXT
        )
    """)
    conn.commit()
    conn.close()

inicializar_db()

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

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Estação Meteorológica & IA</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <meta http-equiv="refresh" content="60">
        <style>
            body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f0f2f5; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .full-width { grid-column: span 2; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border-bottom: 1px solid #ddd; padding: 12px; text-align: center; }
            th { background-color: #007BFF; color: white; border-radius: 4px 4px 0 0; }
            .ia-card { text-align: center; border: 2px solid; }
            .porcentagem { font-size: 4em; font-weight: bold; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>⛅ Estação Meteorológica Inteligente</h1>
        
        <div class="grid">
            <div class="card ia-card" style="background-color: {{ cor_card }}; border-color: {{ cor_texto }}; color: {{ cor_texto }}">
                <h3>🤖 IA: Chance de Chuva</h3>
                <div class="porcentagem">{{ "%.1f"|format(prob_chuva) }}%</div>
                <div style="font-weight: bold; font-size: 1.2em;">{{ msg_previsao }}</div>
                <br>
                <small>
                    <strong>Médias Usadas (60min):</strong><br>
                    Temp: {{ "%.1f"|format(inputs_usados[0]) }}°C | 
                    Umid: {{ "%.1f"|format(inputs_usados[1]) }}% <br> 
                    Press: {{ "%.1f"|format(inputs_usados[2]) }} hPa |
                    Vento: {{ "%.1f"|format(inputs_usados[3]) }} m/s
                </small>
            </div>

            <div class="card" style="background: #e3f2fd; border-left: 5px solid #2196F3;">
                <h3>🌬️ Vento em {{ cidade }}</h3>
                <p>Média dos últimos 60min:</p>
                <div style="font-size: 3em; font-weight: bold; color: #1565C0;">
                    {{ "%.1f"|format(inputs_usados[3]) }} m/s
                </div>
                <small>Fonte: OpenWeatherMap (Integrado)</small>
            </div>

            <div class="card full-width">
                <h3>📊 Tempo Real (Última Hora)</h3>
                <canvas id="grafico" height="80"></canvas>
            </div>
        </div>

        <div class="card full-width">
            <h3>📑 Histórico de Médias (Arquivadas)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Período</th>
                        <th>Temp</th>
                        <th>Pressão</th>
                        <th>Umid</th>
                        <th>Vento Média</th> <th>Amostras</th>
                    </tr>
                </thead>
                <tbody>
                    {% for r in resumos %}
                    <tr>
                        <td>{{ r[1].split('T')[1][:5] }} - {{ r[2].split('T')[1][:5] }}</td>
                        <td>{{ "%.1f"|format(r[3]) }} °C</td>
                        <td>{{ "%.1f"|format(r[4]) }} hPa</td>
                        <td>{{ "%.1f"|format(r[6]) }} %</td>
                        
                        <td><strong>{{ "%.1f"|format(r[7]) }} m/s</strong></td>
                        
                        <td>{{ r[8] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <script>
            let ctx = document.getElementById('grafico').getContext('2d');
            let chart = new Chart(ctx, {
                type: 'line',
                data: { labels: [], datasets: [ 
                    { label: 'Temp', data: [], borderColor: 'red', yAxisID: 'y' }, 
                    { label: 'Umid', data: [], borderColor: 'blue', yAxisID: 'y' },
                    { label: 'Vento', data: [], borderColor: 'orange', yAxisID: 'y' } 
                ]},
                options: { animation: false }
            });

            function atualizarGrafico() {
                fetch("/api/brutos").then(res => res.json()).then(dados => {
                    let labels = [], temp = [], umid = [], vento = [];
                    dados.reverse().forEach(d => {
                        labels.push(d[6].split('T')[1].split('.')[0]); // Data é indice 6 agora
                        temp.push(d[1]); 
                        umid.push(d[4]); 
                        vento.push(d[5]); // Vento é indice 5
                    });
                    chart.data.labels = labels; 
                    chart.data.datasets[0].data = temp; 
                    chart.data.datasets[1].data = umid; 
                    chart.data.datasets[2].data = vento;
                    chart.update();
                });
            }
            setInterval(atualizarGrafico, 3000);
            atualizarGrafico();
        </script>
    </body>
    </html>
    """
    return render_template_string(html, 
                                  resumos=resumos, 
                                  prob_chuva=prob_chuva, 
                                  msg_previsao=msg_previsao,
                                  cor_card=cor_card,
                                  cor_texto=cor_texto,
                                  inputs_usados=inputs_usados,
                                  cidade=cidade_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
