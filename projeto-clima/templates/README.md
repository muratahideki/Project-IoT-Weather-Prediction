# Documentação do Dashboard (Frontend)

O arquivo `dashboard.html` é a interface visual da estação meteorológica. Ele não é apenas uma página estática; é um **template dinâmico** renderizado pelo Flask (Python) que utiliza tecnologias modernas para exibir dados em tempo real.

## Tecnologias Utilizadas

* **HTML5 & CSS3:** Layout responsivo utilizando **CSS Grid** para organizar os cartões de informação.
* **Jinja2 (Template Engine):** Linguagem de templating do Python que injeta dados do servidor diretamente no HTML antes de ele chegar ao navegador.
* **Chart.js:** Biblioteca JavaScript para renderização do gráfico de linhas (Temperatura, Umidade e Vento).
* **Fetch API:** JavaScript moderno para buscar dados novos (AJAX) sem precisar recarregar a página inteira.

## Lógica de Funcionamento

O frontend opera em duas camadas de atualização de dados:

### 1. Renderização no Servidor (Server-Side)
Ao carregar a página, o Flask processa o HTML e substitui as variáveis "placeholder" pelos valores calculados no Backend.

* **Lógica de Cores e Alertas:**
    O Python decide a cor dos cartões antes de enviar o HTML. Se a probabilidade de chuva for alta, o cartão já nasce vermelho.
    ```html
    <div style="background-color: {{ cor_card }}; color: {{ cor_texto }}">
        {{ msg_previsao }}
    </div>
    ```
* **Tabela de Histórico:**
    Um loop `{% for %}` percorre a lista de médias arquivadas no banco de dados SQLite e cria as linhas da tabela dinamicamente.

### 2. Atualização em Tempo Real (Client-Side)
Para o gráfico de "Tempo Real" (última hora), a página não precisa de refresh. Um script JavaScript roda em segundo plano:

1.  Um temporizador (`setInterval`) é acionado a cada **3 segundos**.
2.  Ele faz uma requisição assíncrona para a rota `/api/brutos`.
3.  O JSON recebido é processado e o gráfico é redesenhado instantaneamente.

```javascript
// Trecho simplificado da lógica de atualização
function atualizarGrafico() {
    fetch("/api/brutos")
        .then(res => res.json())
        .then(dados => {
            // Atualiza os arrays do Chart.js
            chart.data.datasets[0].data = dados.temp;
            chart.update();
        });
}
````

### 3 Head

A seção <head> está dividido em metadados e em estilo 

```html
<head>
    <meta charset="utf-8">
    <title>Estação Meteorológica & IA</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <meta http-equiv="refresh" content="60">
    <style>
        body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f0f2f5; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .full-width { grid-column: span 2; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border-bottom: 1px solid #ddd; padding: 12px; text-align: center; }
        th { background-color: #007BFF; color: white; border-radius: 4px 4px 0 0; }
        .ia-card { text-align: center; border: 2px solid; }
        .porcentagem { font-size: 4em; font-weight: bold; margin: 10px 0; }
    </style>
</head>
```
#### 3.1 Metadados 

`<meta charset="utf-8">`: Define a codificação de caracteres da página. Permite usar acentos, ç, símbolos e caracteres especiais corretamente.
`<title>Estação Meteorológica & IA</title>`: vai aparecer como nome na aba do navegador <br>
`<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`: Está importando a biblioteca chart.js, usado para criar gráficos.<br>
`<meta http-equiv="refresh" content="60">`: atualiza a página a cada 60s 

#### 3.2 Estilo 

Essa parte está dubdividida em <style> onde é usado o CSS

`body`<br>
Temos fonte moderna, espaçamento interno, fundo cinza claro

```css
body {
  font-family: 'Segoe UI', sans-serif;
  padding: 20px;
  background: #f0f2f5;
}
```

`.grid`<br>
Cria um design em grade: duas coluna iguais e epaço entre os cards (por causa de 1fr 1fr, na proporção de 1:1, ou 50%)<br>
Além disso, temos um gap de 20 px, isto é, uma distância de 20 pix entre as colunas

```css
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
```

`.card`<br>
Fundo branco, cantos arredondados, sombra leve 

```css
.card {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

`.full-width`<br>
Faz um card ocupar as duas colunas da grid.

```css
.full-width {
  grid-column: span 2;
}
```

`table`<br>
Estiliza tabelas, ocupando 100% da largura, remove espaço entre bordas, com uma margem no topo de 10px 
```css
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
```

`th, td`<br>
Estilo das célula: Linha separadora, Espaçamento interno, Texto centralizado

```css
th, td {
  border-bottom: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}
```

`th`<br>
Cabeçalho da tabela: Azul, Texto branco, Cantos arredondados no topo.

```css
th {
  background-color: #007BFF;
  color: white;
  border-radius: 4px 4px 0 0;
}
```

`.ia-card`<br>
Um card especial para IA: Conteúdo centralizado, Borda visível (pode mudar cor conforme status)

```css
.ia-card {
  text-align: center;
  border: 2px solid;
}

```

`.porcentagem`<br>

```css
.porcentagem {
  font-size: 4em;
  font-weight: bold;
  margin: 10px 0;
}
```

### BODY 

```html
<div class="grid">
    <div class="card ia-card" style="background-color: {{ cor_card }}; border-color: {{ cor_texto }}; color: {{ cor_texto }}">
        <h3>🤖 IA: Chance de Chuva</h3>
        <div class="porcentagem">{{ "%.1f"|format(prob_chuva) }}%</div>
        <div style="font-weight: bold; font-size: 1.2em;">{{ msg_previsao }}</div>
        <br>
        <small>
            <strong>Médias Usadas (60min):</strong><br>
            Temp: {{ "%.1f"|format(inputs_usados[0]) }}°C | 
            Umid: {{ "%.1f"|format(inputs_usados[1]) }}% <br> 
            Press: {{ "%.1f"|format(inputs_usados[2]) }} hPa |
            Vento: {{ "%.1f"|format(inputs_usados[3]) }} m/s
        </small>
    </div>
```

Vamos analisar uma parte do body<br>
`<div class="porcentagem">{{ "%.1f"|format(prob_chuva) }}%</div>`: o que está dentro das chaves mostra que é um float, e vai ser usado até a primeira casa decimal de prob_chuva. Mas de onde vem prob_chuva e as outras váriáveis? A seguir mostra uma parte do código da routes, em um arquivo chamado api.py. Nesse parte do código ele chama a função de média móvel dos últimos 60 minutos e chama uma outra função para calcular a probabilidade de chuva.

```python 
    return render_template(
        "dashboard.html",
        prob_chuva=prob_chuva,
        msg_previsao=msg_previsao,
        cor_card=cor_card,
        cor_texto=cor_texto,
        inputs_usados=inputs_usados,
    )
```

A parte central aqui é o que retorna, uma função nativa do flask que faz a comunicação com html, chama-se render_template(). Essa função vai procurar o arquivo "dashboard.html" na pasta template e vai mandar todas as variáveis presentes como argumentos dessa função. 

### Gráfico 

Em seguida temos um card para velocidade de vento, mas não tem nenhuma novidade no código. Passamos então para o código do gráfico a seguir:

```html
        <div class="card full-width">
            <h3> Tempo Real (Última Hora)</h3>
            <canvas id="grafico" height="80"></canvas>
        </div>
```

O que importa é esse id="gráfico, por causa do javascript que de fato monta o gráfico:

```js
let ctx = document.getElementById('grafico').getContext('2d');
let chart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [ 
        { label: 'Temp', data: [], borderColor: 'red', yAxisID: 'y' }, 
        { label: 'Umid', data: [], borderColor: 'blue', yAxisID: 'y' },
        { label: 'Vento', data: [], borderColor: 'orange', yAxisID: 'y' } 
    ]},
    options: { animation: false }
});
```

- getElementById procura no html onde está o id "gráfico
- getContext se relaciona com chart.js para criar os desenhos 2D
- Em `new Chart(ctx, ` o primeiro parâmetro ctx indica onde vai ser desenhado, enquanto o segundo indica as configurações
- `type: 'line '` indica que o gráfico vai ser de linha.
- `labels: []` é o eixo x que está vázio porque vai ser preenchido dinamicamente com o horário.
- temos 3 variáveis para oo gráfico, cada um representado pela mesma cor, tendo o mesmo eixo y de referência e também valores de data vázios pois vão ser adicionados dinamicamente.

Em seguida temos uma função que vai buscar os dados para preencher o gráfico
```js
function atualizarGrafico() {
    fetch("/api/brutos").then(res => res.json()).then(dados => {
        let labels = [], temp = [], umid = [], vento = [];
        dados.reverse().forEach(d => {
            labels.push(d[6].split('T')[1].split('.')[0]); // Data é indice 6 agora
            temp.push(d[1]); 
            umid.push(d[4]); 
            vento.push(d[5]); // Vento é indice 5
        });
        chart.data.labels = labels; 
        chart.data.datasets[0].data = temp; 
        chart.data.datasets[1].data = umid; 
        chart.data.datasets[2].data = vento;
        chart.update();
    });
}

setInterval(atualizarGrafico, 3000);
atualizarGrafico();
```

- A busca ocorre em uma rota onde pega os valores da tabela medidas, e seleciona as últimas 60 ( o gráfico vai ter esse intervalo de 60 medidas portanto)
- fetch() faz uma requisição HTTP (GET por padrão). "/api/brutos" é o endpoint do seu backend (ex: Flask). É esperado um json
- A resposta que é recebida chama-se response. Por isso em `then()` a res é transformada em um objeto javascript
- Em seguida eu crio uma variável dados que vai receber os json, se tornando um array de array de medidas , algo como:

```
dados = [
  [
    0,          // índice 0 → algum id
    25.3,       // índice 1 → temperatura
    ...,        // índice 2
    ...,        // índice 3
    62,         // índice 4 → umidade
    4.8,        // índice 5 → vento
    "2025-01-02T14:30:10.123" // índice 6 → data/hora
  ],
  ...
]
```

- Logo em seguida são criado arrays de interesse, que vão representar as variáveis do gráfico.
- `dados.reverse().forEach(d => {` desse objeto dados vou pegar o mais recente com o uso de reverse(). Para cada array que vai ser chamado de d:
- d[6] → campo de data/hora (ISO, ex: 2025-01-02T14:23:10.123)
- .split('T')[1] → pega só a hora (14:23:10.123)
- .split('.')[0] → remove os milissegundos
- é usado o push para adicionar ao array
- chart é basicamente o gráfico, o .data é o atributo de valor
- chart.update vai atualizar o gráfico
