from flask import Blueprint, render_template
from datetime import datetime, timedelta

from repository.medidas_repo import obter_media_movel
from services.climas_service import calcular_probabilidade_chuva

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():

    media = obter_media_movel(60)

    prob_chuva = 0.0
    msg_previsao = "Aguardando dados..."
    cor_card = "#eeeeee"
    cor_texto = "#333333"
    inputs_usados = [0, 0, 0, 0]

    if media and media[0] is not None:
        t, u, p, v = media
        inputs_usados = [t, u, p, v]

        prob_chuva = calcular_probabilidade_chuva(t, u, p, v)

        if prob_chuva > 50:
            cor_card = "#ffcccc"
            cor_texto = "#a00000"
            msg_previsao = "ALTA probabilidade de chuva"
        else:
            cor_card = "#ccffcc"
            cor_texto = "#006600"
            msg_previsao = "Baixa probabilidade de chuva"

    return render_template(
        "dashboard.html",
        prob_chuva=prob_chuva,
        msg_previsao=msg_previsao,
        cor_card=cor_card,
        cor_texto=cor_texto,
        inputs_usados=inputs_usados,
    )
