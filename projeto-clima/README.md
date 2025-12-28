### 1- Arquitetura do projeto 

projeto-clima/<br>
│<br>
├── app.py<br>
├── requirements.txt<br>
├── Dockerfile<br>
├── docker-compose.yml  <br> 
│<br>
├── routes/<br>
├── services/<br>
├── repositories/<br>
├── database/<br>
├── templates/<br>
├── static/<br>
└── data/<br>
    └── clima.db<br>


### 2- routes

Em routes temos dois arquivos principais `app.py` e `dashboard.py` (explicação no README.md de templates). O app.py usa o Blueprint para organizar as rotas. Isso impede que o código principal fica com muita informação (das rotas)

```py
from flask import Blueprint, request, jsonify
from repository.medidas_repo import salvar_medida, obter_medidas_brutas

api_bp = Blueprint("api", __name__)

@api_bp.route("/dados", methods=["POST"])
def receber_dados():
    dados = request.get_json()
    salvar_medida(dados)

@api_bp.route("/api/brutos") # aqui está por defaut o method get 
def api_brutos():
    return jsonify(obter_medidas_brutas())
```

Estamos indicando pelo decorador que se for usado o método HTTP, na rota indicadao, vai ser chamada as funções: ou receber_dados() que vai armazenar um json na variável dados.<br>
Vamos entender o que faz as funções salvar medida() e obter_medidas_brutas() no próximo tópico de repository.

### repository

No repositório temos um arquivo chamado de medidas repo, onde que tem as funções salvar medida() e obter_medidas_brutas() do tópico anterior.

```py
import sqlite3
from datetime import datetime, timedelta

DB_NAME = "estacao.db"

def salvar_medida(
    temperatura: float,
    pressao: float,
    altitude: float,
    umidade: float,
    vento: float
) -> None:
    """
    Salva uma medida bruta no banco de dados.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO medidas
        (temperatura, pressao, altitude, umidade, vento, data_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        temperatura,
        pressao,
        altitude,
        umidade,
        vento,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
```
