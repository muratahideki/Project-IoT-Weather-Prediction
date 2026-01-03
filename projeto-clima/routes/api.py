from flask import Blueprint, render_template, request, jsonify
from repository.medidas_repo import salvar_medida, obter_medidas_brutas, obter_media_movel
from services.vento_service import obter_vento_externo

from services.climas_service import calcular_probabilidade_chuva

api_bp = Blueprint("api", __name__)

@api_bp.route("/dados", methods=["POST"])
def receber_dados():
    dados = request.get_json()

    # 1. Pega os dados do ESP32
    temp = dados.get("temp")
    press = dados.get("pressao")
    alt = dados.get("altitude")
    umid = dados.get("umidade")

    vento_atual, _ = obter_vento_externo()


    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    salvar_medida(temp, press, alt, umid, vento_atual) # essa função está salvando a medida na tabela medidas 
    return jsonify({"status": "ok"})


@api_bp.route("/api/brutos")
def api_brutos():
    return jsonify(obter_medidas_brutas())


@api_bp.route("/" )
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