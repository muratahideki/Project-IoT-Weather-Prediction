import sqlite3
from datetime import datetime

DB_NAME = "estacao.db"

def salvar_resumo(
    temperatura: float,
    umidade: float,
    pressao: float,
    vento: float,
    data_hora: str | None = None
) -> None:
    """
    Salva um resumo (ex: média horária) no banco.
    """
    if data_hora is None:
        data_hora = datetime.now().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resumos
        (temperatura, umidade, pressao, vento, data_hora)
        VALUES (?, ?, ?, ?, ?)
    """, (
        temperatura,
        umidade,
        pressao,
        vento,
        data_hora
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
        ORDER BY data_hora DESC
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
        ORDER BY data_hora DESC
        LIMIT 1
    """)

    dado = cursor.fetchone()
    conn.close()

    return dado
