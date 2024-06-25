-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS sistema_filmes;
USE sistema_filmes;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL, -- Campo para senha em hash
    tipo_conta BOOLEAN NOT NULL DEFAULT 0
);

-- Tabela de Filmes
CREATE TABLE IF NOT EXISTS filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    ano INT NOT NULL CHECK (ano >= 1888 AND ano <= YEAR(CURDATE())), -- Filme mais antigo e o ano atual
    descricao TEXT,
    genero VARCHAR(255),
    caminho_imagem VARCHAR(255),
    url_trailer VARCHAR(255) 
);

-- Tabela Avaliações
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_filme INT NOT NULL,
    nota FLOAT NOT NULL CHECK (nota >= 0 AND nota <= 10),
    data_avaliacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_filme) REFERENCES filmes(id),
    UNIQUE(id_usuario, id_filme) -- Usuário pode avaliar um filme apenas uma vez
);

-- Tabela Comentários
CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_filme INT NOT NULL,
    comentario TEXT NOT NULL,
    data_comentario DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_filme) REFERENCES filmes(id)
);