Pré-requisitos
Python 3.x
Flask
Flask-MySQLdb
Flask-Cors
Flask-JWT-Extended
Instalação
Clone o repositório:

git clone https://github.com/LinikerOliva/ProjetoAPI.git

pip install -r requirements.txt

Configure o banco de dados MySQL:

Certifique-se de ter um servidor MySQL em execução localmente ou em uma instância remota.
Crie um novo banco de dados com o nome cinema_app.

Abra o arquivo app.py e ajuste as configurações do banco de dados na seção # Configurações do banco de dados.
Gere as chaves secretas:

Abra o arquivo app.py e execute a função generate_secret_key() para gerar chaves secretas para JWT_SECRET_KEY e SECRET_KEY.
Substitua as chaves no arquivo app.py pelas chaves geradas.
Execute a aplicação:

python app.py

Acesse os endpoints da API em http://127.0.0.1:5501/index.html
Uso
A API oferece os seguintes endpoints:

/register: Registra um novo usuário.

/register-admin: Registra um novo usuário com privilégios de administrador.

/login: Autentica um usuário e fornece um token de acesso JWT.

/logout: Faz logout do usuário atual.

/usuarios: Retorna todos os usuários cadastrados.

/usuarios/<id>: Retorna informações sobre um usuário específico.

/usuarios/<id> (PUT): Atualiza as informações de um usuário específico.

/usuarios/<id> (DELETE): Exclui um usuário específico.

/filmes: Retorna todos os filmes cadastrados.

/filmes/<id>: Retorna informações sobre um filme específico.

/filmes (POST): Adiciona um novo filme.

/filmes/<id> (PUT): Atualiza as informações de um filme específico.

/filmes/<id> (DELETE): Exclui um filme específico.

/avaliacoes: Adiciona uma nova avaliação de um filme.

/avaliacoes/<filme_id>: Retorna todas as avaliações de um filme específico.

/comentarios: Adiciona um novo comentário sobre um filme.

/comentarios/<filme_id>: Retorna todos os comentários de um filme específico.

Créditos
Desenvolvido por:

Liniker Rafael Cordeiro Oliva
Miguel Fernandes de Oliveira
João Victor Garbim Ribeiro