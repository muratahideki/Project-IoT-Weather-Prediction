# database.py
import sqlite3
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "data", "estacao.db")

# print("DB PATH:", DB_NAME)


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
            umidade_media REAL,
            vento_medio REAL,
            qnt_amostras INTEGER,
            data_geracao TEXT
        )
    """)

    conn.commit()
    conn.close()
