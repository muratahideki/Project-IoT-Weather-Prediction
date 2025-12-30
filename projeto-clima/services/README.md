### Climas_service

Nesse módulo, é definido a função do cálculo de probabilidade, usando a Regressão logística. 

### Scheduler

Scheduler é um objeto, em que vai funcionar como agendador a partir do atributo add_job. Basicamente ele vai chamar a funçao 
calcular_media_hora_anterior(), quando for horário exato, por causa do argumento minute=0. 

```py
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=calcular_media_hora_anterior,
    trigger="cron",
    minute=0
)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())
```

Assim, toda hora exata ele vai chamar a função calcular_media_hora_anterior que é composta pelo uso de duas funções. 

1) A primeira é obter_media_movel(), que vai calcular a média dos últimos 60 valores (no máximo). Mas como essa função só 
é chamada nos horários exatos, temos a média de cada hora exata. Lembrando que essa função pega os valores da tabela medidas,
ela filtra os últimos valores e faz uma média.
2) A segunda função é salvar os valores na tabela resumos, usando a função salvar_resumos()

Para finanizar, atexit.register(lambda: scheduler.shutdown()) registra uma função que será chamada automaticamente quando o programa encerrar, garantindo que o scheduler seja finalizado corretamente e sem deixar threads abertas.

### Vento Service

Usando API, o método get vai receber informações da velocidade de vento. 

Esta função consulta a API do **OpenWeatherMap** para obter informações de vento em tempo real a partir de uma localização fixa (latitude e longitude) e retorna a velocidade do vento junto com o nome da cidade.

O processo começa montando a URL da requisição HTTP, incluindo:
- o endpoint `/weather` da API,
- as coordenadas geográficas (`lat` e `lon`),
- a unidade de medida em sistema métrico (`units=metric`),
- e a chave de autenticação (`appid`), lida a partir da configuração da aplicação (`Config.WEATHER_API_KEY`).

Em seguida, a função faz uma requisição GET usando a biblioteca `requests`, com um tempo limite de 5 segundos para evitar que a aplicação fique bloqueada caso a API não responda. O método `raise_for_status()` verifica se a resposta HTTP indica sucesso; caso contrário, uma exceção é lançada.

Se a requisição for bem-sucedida, a resposta é convertida para JSON e os dados relevantes são extraídos:
- `data["wind"]["speed"]` fornece a velocidade do vento em metros por segundo,
- `data["name"]` fornece o nome da cidade correspondente às coordenadas consultadas.

Esses dois valores são retornados como uma tupla `(vento, cidade)`.

Todo o código está envolvido em um bloco `try/except` para garantir robustez. Se ocorrer qualquer erro — como falha de rede, chave de API inválida ou formato inesperado da resposta — a função captura a exceção, exibe uma mensagem de erro no console e retorna valores padrão (`0` para o vento e `"Indisponível"` para a cidade), evitando que a aplicação quebre.

