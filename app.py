from flask import Flask, request, jsonify, session, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets, string

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cinema_app'
app.config['JWT_SECRET_KEY'] = generate_secret_key()
app.config['SECRET_KEY'] = generate_secret_key()

mysql = MySQL(app)
jwt = JWTManager(app)
class Filme:
    def __init__(self, id, titulo, ano, descricao, genero, caminho_imagem, url_trailer):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.descricao = descricao
        self.genero = genero
        self.caminho_imagem = caminho_imagem
        self.url_trailer = url_trailer

class Avaliacao:
    def __init__(self, id, id_usuario, id_filme, nota, data_avaliacao):
        self.id = id
        self.id_usuario = id_usuario
        self.id_filme = id_filme
        self.nota = nota
        self.data_avaliacao = data_avaliacao
        
class Comentario:
    def __init__(self, id, id_usuario, id_filme, comentario, data_comentario):
        self.id = id
        self.id_usuario = id_usuario
        self.id_filme = id_filme
        self.comentario = comentario
        self.data_comentario = data_comentario

class Usuario:
    def __init__(self, id, nome, email, is_admin):
        self.id = id
        self.nome = nome
        self.email = email
        self.is_admin = is_admin

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = generate_password_hash(data['senha'])

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'})

@app.route('/register-admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = generate_password_hash(data['senha'])
    is_admin = data.get('is_admin', False)  # Assume False se não especificado

    if is_admin not in [True, False]:
        return jsonify({'error': 'Campo "is_admin" deve ser booleano.'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha, is_admin) VALUES (%s, %s, %s, %s)", (nome, email, senha, is_admin))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    senha = data['senha']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, senha FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()  # Retorna uma tupla (id, senha)
    cursor.close()

    if user and check_password_hash(user[1], senha):  # Acessa a senha pelo índice 1
        access_token = create_access_token(identity=user[0])  # ID do usuário como identidade
        return jsonify({'access_token': access_token, 'user_id': user[0]}), 200  # ID do usuário pelo índice 0
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200


# Usuarios

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nome, email, is_admin FROM usuarios")
    usuarios_data = cursor.fetchall()
    cursor.close()

    usuarios = []
    for id_, nome, email, is_admin in usuarios_data:
        tipo_conta = 'Administrador' if is_admin else 'Usuário'
        usuarios.append({'id': id_, 'nome': nome, 'email': email, 'tipo_conta': tipo_conta})

    return jsonify({'usuarios': usuarios})

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nome, email, is_admin FROM usuarios WHERE id = %s", (usuario_id,))
        usuario_data = cursor.fetchone()
        cursor.close()

        if usuario_data:
            id_, nome, email, is_admin = usuario_data
            tipo_conta = 'Administrador' if is_admin else 'Usuário'
            usuario = Usuario(id_, nome, email, tipo_conta)
            return jsonify({'usuario': usuario.__dict__})
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = generate_password_hash(data['senha'])
    is_admin = data['is_admin']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET nome = %s, email = %s, senha = %s, is_admin = %s WHERE id = %s", (nome, email, senha, is_admin, usuario_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Usuário atualizado com sucesso!'})

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def excluir_usuario(usuario_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Filme excluído com sucesso!'})

# Filmes

@app.route('/filmes', methods=['GET'])
def listar_filmes():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, titulo, ano, descricao, genero, caminho_imagem, url_trailer FROM filmes")
    filmes_data = cursor.fetchall()
    cursor.close()

    filmes = [Filme(id_, titulo, ano, descricao, genero, caminho_imagem.decode() if isinstance(caminho_imagem, bytes) else caminho_imagem, url_trailer) for id_, titulo, ano, descricao, genero, caminho_imagem, url_trailer in filmes_data]

    return jsonify({'filmes': [filme.__dict__ for filme in filmes]})

@app.route('/filmes/<int:filme_id>', methods=['GET'])
def buscar_filme(filme_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, titulo, ano, descricao, genero, caminho_imagem, url_trailer FROM filmes WHERE id = %s", (filme_id,))
    filme_data = cursor.fetchone()
    cursor.close()
    
    if filme_data:
        id, titulo, ano, descricao, genero, caminho_imagem, url_trailer = filme_data
        if isinstance(caminho_imagem, bytes):
            caminho_imagem = caminho_imagem.decode()  # Converte bytes para string
        filme = Filme(id, titulo, ano, descricao, genero, caminho_imagem, url_trailer)
        return jsonify({'filme': filme.__dict__})
    else:
        return jsonify({'message': 'Filme não encontrado'}), 404
    
@app.route('/filmes', methods=['POST'])
def adicionar_filme():
    data = request.get_json()
    titulo = data['titulo']
    descricao = data['descricao']
    ano = data['ano']
    genero = data['genero']
    caminho_imagem = data['caminho_imagem']
    url_trailer = data['url_trailer']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO filmes (titulo, descricao, ano, genero, caminho_imagem, url_trailer) VALUES (%s, %s, %s, %s, %s, %s)", (titulo, descricao, ano, genero, caminho_imagem, url_trailer))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Filme adicionado com sucesso!'})

@app.route('/filmes/<int:filme_id>', methods=['PUT'])
def atualizar_filme(filme_id):
    data = request.get_json()
    titulo = data['titulo']
    descricao = data['descricao']
    ano = data['ano']
    genero = data['genero']
    caminho_imagem = data['caminho_imagem']
    url_trailer = data['url_trailer']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE filmes SET titulo = %s, descricao = %s, ano = %s, genero = %s, caminho_imagem = %s, url_trailer = %s WHERE id = %s", (titulo, descricao, ano, genero, caminho_imagem, url_trailer, filme_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Filme atualizado com sucesso!'})

@app.route('/filmes/<int:filme_id>', methods=['DELETE'])
def excluir_filme(filme_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM filmes WHERE id = %s", (filme_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Filme excluído com sucesso!'})


# Avaliação

@app.route('/avaliacoes', methods=['POST'])
@jwt_required()
def adicionar_avaliacao():
    data = request.get_json()
    id_filme = data['id_filme']
    nota = data['nota']

    current_user_id = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO avaliacoes (id_usuario, id_filme, nota) VALUES (%s, %s, %s)", (current_user_id, id_filme, nota))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Avaliação adicionada com sucesso!'})

@app.route('/avaliacoes/<int:filme_id>', methods=['GET'])
def listar_avaliacoes(filme_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, id_usuario, nota, data_avaliacao FROM avaliacoes WHERE id_filme = %s", (filme_id,))
    avaliacoes_data = cursor.fetchall()
    avaliacoes = []
    for avaliacao in avaliacoes_data:
        id, id_usuario, nota, data_avaliacao = avaliacao
        avaliacoes.append(Avaliacao(id, id_usuario, filme_id, nota, data_avaliacao))
    cursor.close()

    return jsonify({'avaliacoes': [avaliacao.__dict__ for avaliacao in avaliacoes]})

@app.route('/comentarios', methods=['POST'])
@jwt_required()
def adicionar_comentario():
    data = request.get_json()
    id_filme = data['id_filme']
    comentario = data['comentario']

    current_user_id = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO comentarios (id_usuario, id_filme, comentario) VALUES (%s, %s, %s)", (current_user_id, id_filme, comentario))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Comentário adicionado com sucesso!'})

@app.route('/comentarios/<int:filme_id>', methods=['GET'])
def listar_comentarios(filme_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, id_usuario, comentario, data_comentario FROM comentarios WHERE id_filme = %s", (filme_id,))
    comentarios_data = cursor.fetchall()
    comentarios = []
    for comentario in comentarios_data:
        id, id_usuario, comentario, data_comentario = comentario
        comentarios.append(Comentario(id, id_usuario, filme_id, comentario, data_comentario))
    cursor.close()

    return jsonify({'comentarios': [comentario.__dict__ for comentario in comentarios]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)