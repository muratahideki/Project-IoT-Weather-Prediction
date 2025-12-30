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

### config 

Este arquivo define a **configuração central da aplicação**, concentrando variáveis sensíveis, parâmetros do Flask e integrações externas em uma única classe, seguindo um padrão comum em projetos Flask.

Inicialmente, o módulo `os` é utilizado para obter informações do sistema de arquivos e variáveis de ambiente. A constante `BASE_DIR` armazena o caminho absoluto do diretório onde o arquivo de configuração está localizado, permitindo construir caminhos de forma portátil, independentemente do sistema operacional.

A classe `Config` encapsula todas as configurações da aplicação. O atributo `SECRET_KEY` é usado pelo Flask para segurança (por exemplo, sessões e cookies assinados). Ele é lido a partir da variável de ambiente `SECRET_KEY` e, caso não exista, assume um valor padrão apenas para desenvolvimento, deixando explícito que não deve ser usado em produção.

As opções `DEBUG` e `TESTING` controlam o comportamento do Flask, indicando que a aplicação está configurada para execução normal, fora de ambiente de testes ou depuração.

A configuração do banco de dados é feita por meio de `SQLALCHEMY_DATABASE_URI`. Primeiro, o código tenta usar a variável de ambiente `DATABASE_URL`, o que facilita o uso em produção ou em serviços externos. Caso essa variável não esteja definida, é utilizado um banco SQLite local, cujo arquivo (`database.db`) é criado no diretório base do projeto. A opção `SQLALCHEMY_TRACK_MODIFICATIONS` é desativada para evitar sobrecarga desnecessária e warnings do SQLAlchemy.

Por fim, o atributo `WEATHER_API_KEY` armazena a chave de acesso para APIs externas, como a API de clima. Essa chave é lida exclusivamente a partir de variáveis de ambiente, evitando que informações sensíveis fiquem hardcoded no código-fonte.





