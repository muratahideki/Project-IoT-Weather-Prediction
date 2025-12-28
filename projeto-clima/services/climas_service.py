def calcular_probabilidade_chuva(
    temperatura,
    umidade,
    pressao,
    vento
):
    """
    Modelo simples heurístico
    Retorna probabilidade em %
    """
    prob = 0

    # Umidade alta
    if umidade > 80:
        prob += 30
    elif umidade > 60:
        prob += 15

    # Pressão baixa
    if pressao < 1010:
        prob += 25
    elif pressao < 1015:
        prob += 10

    # Temperatura
    if temperatura < 20:
        prob += 10

    # Vento
    if vento > 8:
        prob += 15

    return min(prob, 100)
