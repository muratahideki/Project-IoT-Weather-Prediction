from flask import Blueprint, request, jsonify
from repository.medidas_repo import salvar_medida, obter_medidas_brutas

api_bp = Blueprint("api", __name__)

@api_bp.route("/dados", methods=["POST"])
def receber_dados():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    salvar_medida(dados)
    return jsonify({"status": "ok"})


@api_bp.route("/api/brutos")
def api_brutos():
    return jsonify(obter_medidas_brutas())
