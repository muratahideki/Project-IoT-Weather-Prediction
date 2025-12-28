import sqlite3
from datetime import datetime, timedelta
from config import Config


DB_NAME = "database.db"


def calcular_media_hora_anterior():
    """
    Calcula médias da última hora e salva na tabela resumos
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        uma_hora_atras = datetime.now() - timedelta(hours=1)

        cursor.execute("""
            SELECT
                AVG(temperatura),
                AVG(umidade),
                AVG(pressao),
                AVG(vento)
            FROM medidas
            WHERE data_hora >= ?
        """, (uma_hora_atras.isoformat(),))

        medias = cursor.fetchone()

        if medias and medias[0] is not None:
            cursor.execute("""
                INSERT INTO resumos
                (temp_media, umid_media, press_media, vento_medio, data_hora)
                VALUES (?, ?, ?, ?, ?)
            """, (*medias, datetime.now().isoformat()))

        conn.commit()
        conn.close()

        print("Resumo horário salvo")

    except Exception as e:
        print("Erro no scheduler:", e)
