from datetime import datetime
from repository import obter_media_movel, salvar_resumo
from apscheduler.schedulers.background import BackgroundScheduler


DB_NAME = "database.db"


def calcular_media_hora_anterior():
    """
    Calcula médias da última hora da tabela medidas, usando o scheduler em horários exatos 
    salva na tabela resumos
    """

    media_temp, media_umidade, media_pressao, media_vento, counts = obter_media_movel()
    salvar_resumo(media_temp, media_umidade, media_pressao, media_vento, counts )

