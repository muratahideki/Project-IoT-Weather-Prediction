import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Segurança
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-dev-nao-usar-em-producao")

    # Flask
    DEBUG = False
    TESTING = False

    # Banco de dados (exemplo SQLite)
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # APIs externas (exemplo clima)
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")