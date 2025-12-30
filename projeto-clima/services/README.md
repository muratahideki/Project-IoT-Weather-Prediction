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

### Vento Service

Usando API, o método get vai receber informações da velocidade de vento. 
