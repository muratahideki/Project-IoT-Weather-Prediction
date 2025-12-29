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

Na função `salvar_medida()`:
- `conn = sqlite3.connect(DB_NAME):` conexão com sqlite3
- `cursor = conn.cursor():` cursor é um objeto é por meio dele vai ocorrer a comunicação e modificação do banco de dados
- `cursor.execute(sql,parametros fornecidos pelo python):` aqui que ocorre o tipo de modificação desejada, além de fazer a comunicação entre sql e python. No sql temos:

```sql
INSERT INTO medidas
    (temperatura, pressao, altitude, umidade, vento, data_hora)
VALUES
    (?, ?, ?, ?, ?, ?)
```
Parte 1 — INSERT INTO medidas<br>

- INSERT INTO → comando de inserção
- medidas → nome da tabela

O SQLite: localiza a tabela medidas, verifica se ela existe, carrega o esquema dela

Parte 2 — Lista de colunas

- `(temperatura, pressao, altitude, umidade, vento, data_hora):` são as colunas que serão preenchidas 

Parte 3 - Placeholders 

- `values` vai indicar que o que vem depois são as valores que vão preencher as colunas, no caso, `(?, ?, ?, ?, ?, ?)` que na verdade são Placeholders.

Para encerrar, `conn.commit()` serve para salvar os dados na tabela; `conn.close()` serve para encerrar a tabela 

Para a seguinte parte do código:

```python
def obter_medidas_brutas(limit: int = 60):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM medidas
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    dados = cursor.fetchall()
    conn.close()

    return dados
```

Vai recuperar os últimos 60 dados, vamos entender a parte do sql:
- `SELECT * FROM medidas:` Seleciona todas as colunas de todas as linhas da tabela medidas
- `ORDER BY id DESC:` Ordena pelo id e na ordem decrescente, isto é, dos mais novos para os mais antigos
- `dados = cursor.fetchall(): ` lê do banco todos os resultados da última consulta SQL executada pelo cursor, e guarda isso em memória dentro da variável dados. O select é como uma seleção pelo curso, mas só com fetchall é que busca e salva na variável.

```
def obter_media_movel(minutos: int = 60):
    """
    Calcula a média das medidas dos últimos X minutos.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inicio = datetime.now() - timedelta(minutes=minutos)

    cursor.execute("""
        SELECT
            AVG(temperatura),
            AVG(umidade),
            AVG(pressao),
            AVG(vento)
        FROM medidas
        WHERE data_hora >= ?
    """, (inicio.isoformat(),))

    media = cursor.fetchone()
    conn.close()

    return media
```
- O AVG faz as médias
- Invés de usar o fetchall(), que é para várias linhas, usa o fetchone() para uma linha
- `inicio = datetime.now() - timedelta(minutes=minutos):` estamos pegando o tempo atual do `datetime.now()` e voltando 1h, e assim falamos que o inicio foi 1h atrás. Isso é feito o tempo todo por isso que a média é móvel.

| Aspecto      | Medidas brutas       | Média móvel               |
| ------------ | -------------------- | ------------------------- |
| Tipo de dado | Linhas reais         | Valores agregados         |
| Critério     | Quantidade (`LIMIT`) | Tempo (`WHERE data_hora`) |
| Funções SQL  | Nenhuma              | `AVG()`                   |
| Fetch        | `fetchall()`         | `fetchone()`              |
| Retorno      | Lista de tuplas      | Uma única tupla           |
| Semântica    | Histórico            | Estatística               |

