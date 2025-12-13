# Estação Meteorológica IoT com Previsão de Chuva (IA)

Este projeto consiste em uma estação meteorológica completa que coleta dados ambientais locais via **ESP32**, enriquece com dados de APIs externas (**OpenWeatherMap**) e utiliza um modelo de **Regressão Logística** para calcular a probabilidade de chuva em tempo real.

O sistema possui um dashboard web para visualização de dados instantâneos e históricos, além de um "robô" (Scheduler) que processa médias horárias automaticamente.

## Funcionalidades

- ** Coleta de Dados IoT:** Recebe Temperatura, Umidade, Pressão e Altitude de um microcontrolador ESP32.
- **cloud Integração via API:** Consulta a velocidade do vento em tempo real via OpenWeatherMap para complementar os dados locais.
- ** IA / Previsão:** Algoritmo de Regressão Logística implementado "from scratch" para calcular a % de chance de chuva baseada em pesos pré-treinados.
- ** Dashboard Interativo:** Gráficos em tempo real (Chart.js) e exibição de cartões de alerta.
- ** Histórico e Automação:** Banco de dados SQLite para armazenar leituras e um Job agendado (APScheduler) que calcula e arquiva médias horárias.

## Arquitetura do Projeto

O projeto segue uma arquitetura cliente-servidor:

1.  **Hardware (Cliente):** O ESP32 lê os sensores e envia um JSON via POST para o servidor.
2.  **Servidor (Flask):**
    * Recebe os dados.
    * Busca dados de vento na API externa.
    * Salva os dados brutos no SQLite.
3.  **Frontend (HTML/JS):** Consome a API do servidor para plotar gráficos e exibir a previsão.
4.  **Background Task:** A cada hora, um script calcula a média dos dados e salva na tabela de resumos.

##  Como Executar

### Pré-requisitos
* Python 3.8+
* Conta na [OpenWeatherMap](https://openweathermap.org/) (para obter a API Key)

### Instalação

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/estacao-meteorologica-ia.git](https://github.com/seu-usuario/estacao-meteorologica-ia.git)
    cd estacao-meteorologica-ia
    ```

2.  Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install flask apscheduler requests
    ```

3.  Configuração:
    Abra o arquivo `app.py` (ou `config.py` se refatorado) e insira sua chave da API:
    ```python
    API_KEY = "SUA_CHAVE_AQUI"
    LAT = "-22.73"  # Sua Latitude
    LON = "-45.12"  # Sua Longitude
    ```

4.  Execute o servidor:
    ```bash
    python app.py
    ```
    O servidor iniciará em `http://0.0.0.0:5000`.

## 📡 API Endpoints (Para o ESP32)

O ESP32 deve enviar uma requisição **HTTP POST** para o endpoint `/dados` com o seguinte formato JSON:

**URL:** `http://SEU_IP:5000/dados`

**Payload JSON:**
```json
{
  "temp": 25.4,
  "umidade": 60.5,
  "pressao": 1013.2,
  "altitude": 520.0
}
