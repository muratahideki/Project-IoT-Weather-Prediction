from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

import database
import tasks

from routes.api import api_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)

# Banco
database.inicializar_db()

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(tasks.calcular_media_hora_anterior, trigger="cron", minute=0)
scheduler.start()

# Blueprints
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
