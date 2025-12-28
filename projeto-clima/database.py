# database.py
import sqlite3
DB_NAME = "estacao.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ---- Tabela medidas ----
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

    # ---- Tabela resumos ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inicio TEXT,
            fim TEXT,
            temp_media REAL,
            pressao_media REAL,
            altitude_media REAL,
            umidade_media REAL,
            vento_medio REAL,
            amostras INTEGER
        )
    """)

    conn.commit()
    conn.close()
