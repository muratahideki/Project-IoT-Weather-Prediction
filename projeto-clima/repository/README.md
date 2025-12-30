### repository

#### medidas_repo.py

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
- O isoformat() transforma o horário em uma string, que é necessário para funcionar no sql. 

| Aspecto      | Medidas brutas       | Média móvel               |
| ------------ | -------------------- | ------------------------- |
| Tipo de dado | Linhas reais         | Valores agregados         |
| Critério     | Quantidade (`LIMIT`) | Tempo (`WHERE data_hora`) |
| Funções SQL  | Nenhuma              | `AVG()`                   |
| Fetch        | `fetchall()`         | `fetchone()`              |
| Retorno      | Lista de tuplas      | Uma única tupla           |
| Semântica    | Histórico            | Estatística               |



#### resumos_repo.py

1) Função salvar_resumos():

Essa função é importante para a persistencia dos valores (ficar salvo na memória)

```py
def salvar_resumo(
    temperatura: float,
    umidade: float,
    pressao: float,
    vento: float,
    data_hora: str | None = None
) -> None:
```
- note que o parâmetro data_hora pode ser uma string ou None, isto é, a função pode ser chamada mesmo sem informar o horário
- A função não retorna nada também

```py
if data_hora is None:
        data_hora = datetime.now().isoformat()
```
- Se não for informado a data, ele pega data do momento e a transforma em string.

```py
cursor.execute("""
        INSERT INTO resumos
        (temperatura, umidade, pressao, vento, data_hora)
        VALUES (?, ?, ?, ?, ?)
    """, (temperatura, umidade, pressao, vento, data_hora
    ))
```

- Note que é parecido com a função salvar_medida(), porém está salvando em uma outra tabela, a de "resumos".

2) Função obter_resumos()

Essa função vai ser análoga a obter_medidas_brutas(), elas usam o sql para selecionar todas as colunas com o "SELECT * FROM ..."
A diferença é que uma vai pegar a função da tabela medidas e esta vai pegar da tabela Resumos. Outra diferença é que, para
o argumento Limit, a outra vai ser 60 (para valor de cada minuto em uma hora) enquanto que esta vai ser 24, para valor de cada hora. 


```py
def obter_resumos(limit: int = 24):
    """
    Retorna os últimos resumos salvos (ex: últimas 24 horas).
    """
```

3) Função obter_ultimo_resumo():

Como o nome diz, ele vai regatar da tabela resumo o valor do último horário

````py
cursor.execute("""
        SELECT *
        FROM resumos
        ORDER BY data_hora DESC
        LIMIT 1
    """)
```

