import unittest
from flask import Flask, jsonify
from seu_arquivo_de_código import app, mysql

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = '123'
        app.config['MYSQL_DB'] = 'cinema_teste'
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_register(self):
        data = {'nome': 'Teste', 'email': 'teste@teste.com', 'senha': 'test123'}
        response = self.app.post('/register', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuário cadastrado com sucesso!', response.json['message'])

    def test_login(self):
        data = {'email': 'teste@teste.com', 'senha': 'test123'}
        response = self.app.post('/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_register_admin(self):
        data = {'nome': 'Admin', 'email': 'admin@admin.com', 'senha': 'admin123', 'is_admin': 1}
        response = self.app.post('/register-admin', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Usuário cadastrado com sucesso!', response.json['message'])

    def test_listar_usuarios(self):
        response = self.app.get('/usuarios')
        self.assertEqual(response.status_code, 200)
        

    def test_adicionar_filme(self):
        data = {'titulo': 'Filme', 'descricao': 'teste', 'ano': 2024, 'genero': 'Ação', 'caminho_imagem': 'https://cdn-amz.woka.io/images/I/71idZRHXljS.jpg'}
        response = self.app.post('/filmes', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Filme adicionado com sucesso!', response.json['message'])

    def test_listar_filmes(self):
        response = self.app.get('/filmes')
        self.assertEqual(response.status_code, 200)
        

    def test_buscar_filme(self):
        response = self.app.get('/filmes/1')
        self.assertEqual(response.status_code, 404)  

    def test_atualizar_filme(self):
        data = {'titulo': 'Transformers', 'descricao': 'Carro se transforma em robo', 'ano': 2023, 'genero': 'Comédia, Terror', 'caminho_imagem': 'https://cdn-amz.woka.io/images/I/71idZRHXljS.jpg'}
        response = self.app.put('/filmes/1', json=data)
        self.assertEqual(response.status_code, 404)  

    def test_excluir_filme(self):
        response = self.app.delete('/filmes/1')
        self.assertEqual(response.status_code, 404)  

    def test_adicionar_avaliacao(self):
        data = {'id_filme': 1, 'nota': 5}
        response = self.app.post('/avaliacoes', json=data)
        self.assertEqual(response.status_code, 404)  

    def test_listar_avaliacoes(self):
        response = self.app.get('/avaliacoes/1')
        self.assertEqual(response.status_code, 404)  

    def test_adicionar_comentario(self):
        data = {'id_filme': 1, 'comentario': 'Ótimo filme!'}
        response = self.app.post('/comentarios', json=data)
        self.assertEqual(response.status_code, 404)  

    def test_listar_comentarios(self):
        response = self.app.get('/comentarios/1')
        self.assertEqual(response.status_code, 404)  

if __name__ == '__main__':
    unittest.main()
