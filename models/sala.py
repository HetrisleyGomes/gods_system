from app import db

class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    nome = db.Column(db.String(50))
    fichas = db.Column(db.Integer, db.ForeignKey('ficha.id'))
    senha = db.Column(db.String(50))


# Nome: Sala
# valores: 'id', integer, chave primária; 'codigo', string(10), unique; 'nome', string(50), 'senha', string(50), 'fichas', será uma coluna de referencia, uma sala pode ter várias fichas, mas uma ficha só pode estar em uma sala
# 
# CREATE TABLE sala (
#     id VARCHAR(36) PRIMARY KEY,
#     codigo VARCHAR(10) UNIQUE NOT NULL,
#     nome VARCHAR(50) NOT NULL,
#     senha VARCHAR(50)
# );