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
`<div class="porcentagem">{{ "%.1f"|format(prob_chuva) }}%</div>`: o que está dentro das chaves mostra que é um float, e vai ser usado até a primeira casa decimal de prob_chuva. Mas de onde vem prob_chuva e as outras váriáveis? A seguir mostra uma parte do código da routes, em um arquivo chamado dashboard.py 

```python 
@dashboard_bp.route("/")
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
```

A parte central aqui é o que retorna, uma função nativa do flask que faz a comunicação com html, chama-se render_template(). Essa função vai procurar o arquivo "dashboard.html" na pasta template e vai mandar todas as variáveis presentes como argumentos dessa função. 

