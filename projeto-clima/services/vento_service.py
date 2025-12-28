import requests
from config import Config


def obter_vento_externo():
    """
    Retorna:
        (vento_em_m_s, nome_da_cidade)
    """
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            "?lat=-23.55&lon=-46.63&units=metric"
            f"&appid={Config.WEATHER_API_KEY}"
        )

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        vento = data["wind"]["speed"]
        cidade = data["name"]

        return vento, cidade

    except Exception as e:
        print("Erro ao obter vento:", e)
        return 0, "Indisponível"
