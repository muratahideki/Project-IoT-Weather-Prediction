import sqlite3
from datetime import datetime, timedelta
from database import DB_NAME

def salvar_resumo(
    temperatura: float,
    umidade: float,
    pressao: float,
    vento: float,
    counts: int
) -> None:
    
    """
    Salva um resumo (ex: média horária) no banco.
    """

    agora = datetime.now()
    data_fim = agora.replace(minute=0, second=0, microsecond=0)
    data_inicio = data_fim - timedelta(hours=1)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumos (inicio, fim, temp_media, pressao_media, umidade_media, vento_medio, qnt_amostras , data_geracao)
        VALUES (?, ?, ?, ?, ?, ?, ?. ?)
    """, (
        data_inicio.isoformat(),
        data_fim.isoformat(),
        temperatura,
        pressao, 
        umidade,
        vento,
        counts,
        agora.isoformat()
    ))

    conn.commit()
    conn.close()


def obter_resumos(limit: int = 24):
    """
    Retorna os últimos resumos salvos (ex: últimas 24 horas).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resumos
        ORDER BY data_geracao DESC
        LIMIT ?
    """, (limit,))

    dados = cursor.fetchall()
    conn.close()

    return dados


def obter_ultimo_resumo():
    """
    Retorna o resumo mais recente.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM resumos
        ORDER BY fim DESC
        LIMIT 1
    """)

    dado = cursor.fetchone()
    conn.close()

    return dado
