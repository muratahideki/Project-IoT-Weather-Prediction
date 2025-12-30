from datetime import datetime
from repository import obter_media_movel, salvar_resumo
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

DB_NAME = "database.db"


def calcular_media_hora_anterior():
    """
    Calcula médias da última hora e salva na tabela resumos
    """

    medias = obter_media_movel()
    salvar_resumo(medias[0], 
                  medias[1],
                  medias[2],
                  medias[3],
                  datetime.now().isoformat())

scheduler = BackgroundScheduler()
scheduler.add_job(func=calcular_media_hora_anterior, trigger="cron", minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
