# database.py
import sqlite3
DB_NAME = "estacao_climatica.db"

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
