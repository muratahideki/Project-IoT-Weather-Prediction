from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import database
from services import calcular_media_hora_anterior

from routes.api import api_bp


app = Flask(__name__)

# Banco
database.inicializar_db()

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=calcular_media_hora_anterior, trigger="cron", minute=0)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Blueprints
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
