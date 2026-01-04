import sqlite3
from datetime import datetime, timedelta
from database import DB_NAME



def salvar_medida(
    temperatura: float,
    pressao: float,
    altitude: float,
    umidade: float,
    vento: float
) -> None:
    """
    Salva uma medida bruta no banco de dados.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medidas
        (temperatura, pressao, altitude, umidade, vento, data_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        temperatura,
        pressao,
        altitude,
        umidade,
        vento,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def obter_medidas_brutas(limit: int = 60):
    """
    Retorna as últimas medidas registradas.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM medidas
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    dados = cursor.fetchall()
    conn.close()

    return dados


def obter_media_movel(minutos: int = 60):
    """
    Calcula a média das medidas dos últimos X minutos.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inicio = datetime.now() - timedelta(minutes=minutos)

    cursor.execute("""
        SELECT
            AVG(temperatura),
            AVG(umidade),
            AVG(pressao),
            AVG(vento),
            COUNT(*)
        FROM medidas
        WHERE data_hora >= ? AND data_hora <= ?
    """, (inicio.isoformat(), datetime().isoformat()))

    media = cursor.fetchone()
    conn.close()

    return media
