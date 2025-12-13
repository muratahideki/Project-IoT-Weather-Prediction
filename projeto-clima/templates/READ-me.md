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
