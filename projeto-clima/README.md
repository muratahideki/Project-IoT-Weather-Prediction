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

### app

Este arquivo é o **ponto de entrada principal da aplicação Flask**, responsável por inicializar o servidor web, preparar o banco de dados, configurar tarefas agendadas e registrar as rotas da API.

A aplicação começa importando o `Flask`, que é o framework responsável por lidar com requisições HTTP, e o `BackgroundScheduler` do APScheduler, utilizado para executar tarefas periódicas em segundo plano sem bloquear o servidor.

Os módulos `database` e `services` são importados para desacoplar responsabilidades: o primeiro cuida da inicialização e acesso ao banco de dados, enquanto o segundo contém funções de processamento agendado, como o cálculo de médias horárias. Essa separação melhora a organização e a manutenibilidade do projeto.

Em seguida, são importados os **Blueprints** (`api_bp`), que encapsula conjuntos de rotas relacionadas. O uso de Blueprints permite dividir a aplicação em módulos independentes, evitando que todas as rotas fiquem concentradas em um único arquivo.

A aplicação Flask é então criada com `app = Flask(__name__)`, o que instancia o servidor e prepara o contexto da aplicação.

Logo após, a função `database.inicializar_db()` é chamada. Isso garante que o banco de dados esteja pronto (por exemplo, com tabelas criadas) **antes** que a aplicação comece a receber requisições ou executar tarefas agendadas.

Na sequência, o scheduler é configurado. Um `BackgroundScheduler` é criado e recebe um job que executa a função `calcular_media_hora_anterior` usando um trigger do tipo `cron`. Com `minute=0`, essa função será chamada automaticamente a cada hora cheia, utilizando o relógio do sistema operacional. O scheduler é iniciado em background, rodando em uma thread separada do Flask.

Depois disso, os Blueprints são registrados na aplicação com `app.register_blueprint(api_bp)`. Esse passo conecta efetivamente as rotas definidas nos módulos externos ao servidor Flask, permitindo que elas respondam a requisições HTTP.

Por fim, o bloco `if __name__ == "__main__":` garante que o servidor Flask só seja iniciado quando este arquivo for executado diretamente. O método `app.run` inicia o servidor escutando em todas as interfaces de rede (`0.0.0.0`), na porta `5000`, com o modo `debug` ativado, o que facilita o desenvolvimento ao permitir recarregamento automático e mensagens de erro detalhadas.

Em conjunto, esse arquivo coordena todo o ciclo de vida da aplicação: inicialização do ambiente, preparação do banco, execução de tarefas periódicas e exposição da API via HTTP.

### config 

Este arquivo define a **configuração central da aplicação**, concentrando variáveis sensíveis, parâmetros do Flask e integrações externas em uma única classe, seguindo um padrão comum em projetos Flask.

Inicialmente, o módulo `os` é utilizado para obter informações do sistema de arquivos e variáveis de ambiente. A constante `BASE_DIR` armazena o caminho absoluto do diretório onde o arquivo de configuração está localizado, permitindo construir caminhos de forma portátil, independentemente do sistema operacional.

A classe `Config` encapsula todas as configurações da aplicação. O atributo `SECRET_KEY` é usado pelo Flask para segurança (por exemplo, sessões e cookies assinados). Ele é lido a partir da variável de ambiente `SECRET_KEY` e, caso não exista, assume um valor padrão apenas para desenvolvimento, deixando explícito que não deve ser usado em produção.

As opções `DEBUG` e `TESTING` controlam o comportamento do Flask, indicando que a aplicação está configurada para execução normal, fora de ambiente de testes ou depuração.

A configuração do banco de dados é feita por meio de `SQLALCHEMY_DATABASE_URI`. Primeiro, o código tenta usar a variável de ambiente `DATABASE_URL`, o que facilita o uso em produção ou em serviços externos. Caso essa variável não esteja definida, é utilizado um banco SQLite local, cujo arquivo (`database.db`) é criado no diretório base do projeto. A opção `SQLALCHEMY_TRACK_MODIFICATIONS` é desativada para evitar sobrecarga desnecessária e warnings do SQLAlchemy.

Por fim, o atributo `WEATHER_API_KEY` armazena a chave de acesso para APIs externas, como a API de clima. Essa chave é lida exclusivamente a partir de variáveis de ambiente, evitando que informações sensíveis fiquem hardcoded no código-fonte.

Para salvar sua chave API:

```powershell
setx WEATHER_API_KEY "sua_chave_aqui"
```

```bash
export WEATHER_API_KEY="sua_chave_aqui"
```

### database 

Cria a tabela de resumos e de medidas 

### dockerfile 

1) Começamos com o `WORKDIR` que basicamente é entrar em um diretório, assim estamos entrando no diretório app.
2) Em seguida fazemos uma `COPY` de requirements.txt e executamos para baixar as libs
3) Fazemos um segundo COPY de todas as pastas e arquivos do códigos com `COPY . .` o primeiro ponto se refere a baixar todos arquivos da pasta e o segundo ponto se refere ao destino da copia em app. (diretório do docker)
- Note que temos assim uma primeira camada de libs e uma segunda dos códigos 

Para fazer funcionar é necessário usar os comados docker build e docker run 

### docker compose 

Se tiver vários conteiners é necessário fazer vários docker run, ou usar um arquivo que automatiza esse processo com docker compose 

1) Começa com services, onde vai ser definido comos os contêineres vão ser usados. Porém só estou usando um serviço que foi nomeado como clima.
- O nome do serviço é qualquer um, mas é indicado um nome da sua função. Esse nome é usado para refernciar quando estiver usando o docker-compose

```bash
docker compose logs clima
docker compose restart clima
```

2) Construir o dockerfile
```bash
    build: .
```
- Vai procurar o dockerfile nessa pasta e buildar
- equivalente à docker build .

3) conteiner_name: clima_app
- opcional
- define o nome do contêiner

4) ports:
- 5000:5000
- porta 5000 da máquina e porta 5000 do docker 

5) volumes:
- ./data: app/data
- isso cria um atalho da pasta do pc ./data e a pasta do contêiner app/data
- Isso permite a persistência de dados, uma vez que pode apagar o contêiner, mas mantendo os dados
- Essa linha é especialmente importante, porque isso mostra que está sendo salvo fora do contêiner, na própria máquina. Isso cria a persistência. 

Para fazer funcionar:

```bash 
docker compose up --build
```

### .dockerignore

evita:
- copiar cache
- copiar configs do VSCode
- copiar arquivos inúteis

```
__pycache__/ 
*.pyc
.env
.git
.gitignore
.vscode```

