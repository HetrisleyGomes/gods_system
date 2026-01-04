from app import db

class Ficha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(
        db.Integer,
        db.ForeignKey('sala.id'),
        nullable=False
    )
    # Infos basicas
    nome_personagem = db.Column(db.String(100))
    vida = db.Column(db.Integer)
    energia = db.Column(db.Integer)
    nivel = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    # Construtores
    cor = db.Column(db.String(20))
    especie = db.Column(db.String(20))
    arquetipo = db.Column(db.String(20))
    # Atributos principais
    forca = db.Column(db.Integer)
    constituicao = db.Column(db.Integer)
    inteligencia = db.Column(db.Integer)
    destreza = db.Column(db.Integer)
    carisma = db.Column(db.Integer)
    # Atributos secundários
    combate = db.Column(db.Integer)
    atletismo = db.Column(db.Integer)
    tecnologia = db.Column(db.Integer)
    percepcao = db.Column(db.Integer)
    conhecimento = db.Column(db.Integer)
    pontaria = db.Column(db.Integer)
    furtividade = db.Column(db.Integer)
    atuacao = db.Column(db.Integer)
    iniciativa  = db.Column(db.Integer)

# Nome: Ficha
# valores: 'id', string(36), chave primária; 'sala_id', referenciando o id da sala; 'poderes' vai refernciar uma tabela extra, já que um poder pode fazer parte de varias fichas e uma ficha pode ter varios poderes;
# 'nome_personagem', string(50); 'vida', int; 'energia', int; 'nivel', int; 'xp', int;
# 'forca', int; 'constituicao', int; 'inteligencia', int; 'destreza', int; 'carisma', int; 
# 'combate', int; 'atletismo', int; 'tecnologia', int; 'percepcao', int; 'conhecimento', int; 'pontaria', int; 'furtividade', int; 'atuacao', int; 'iniciativa', int; 
# 
# CREATE TABLE ficha (
#     id VARCHAR(36) PRIMARY KEY,
#     sala_id VARCHAR(36) NOT NULL,
#     
#     nome_personagem VARCHAR(50) NOT NULL,
#     vida INTEGER,
#     energia INTEGER,
#     nivel INTEGER,
#     xp INTEGER,
# 
#     forca INTEGER,
#     constituicao INTEGER,
#     inteligencia INTEGER,
#     destreza INTEGER,
#     carisma INTEGER,
# 
#     combate INTEGER,
#     atletismo INTEGER,
#     tecnologia INTEGER,
#     percepcao INTEGER,
#     conhecimento INTEGER,
#     pontaria INTEGER,
#     furtividade INTEGER,
#     atuacao INTEGER,
#     iniciativa INTEGER,
# 
#     FOREIGN KEY (sala_id) REFERENCES sala(id)
# );
# 
# nome: poder
# valores: 'id' serial primary key int; 'nome', string(70) not null; 'descrição' aqui vai ser um texto longo, então queria um tipo que não limitasse o tamanho (algo entre 200 e 300 caracteres)
# 
# CREATE TABLE poder (
#     id SERIAL PRIMARY KEY,
#     nome VARCHAR(70) NOT NULL,
#     descricao TEXT
# );
# 
# CREATE TABLE ficha_poder (
#     ficha_id VARCHAR(36) NOT NULL,
#     poder_id INTEGER NOT NULL,
# 
#     PRIMARY KEY (ficha_id, poder_id),
# 
#     FOREIGN KEY (ficha_id) REFERENCES ficha(id),
#     FOREIGN KEY (poder_id) REFERENCES poder(id)
# );
# Parte principal
nome_personagem, vida, energia, armadura, cor, especie, arquetipo
ps: vida e energia vão sendo alterados durante a sessão, então temos que pensar em soluções para permitir alterações (ou por agora apenas deixar esse caminho preparado).
ps: podemos usar o valor da propriedade 'cor' para pôr detalhes da cor associada ao personagem (como uma faixa no topo ou outros detalhes)
# Atributos principais
forca int; constituicao int; inteligencia int; destreza int; carisma int;
#atributos secundários
combate int; atletismo int; tecnologia int; percepcao int; conhecimento int; pontaria int; furtividade int; atuacao int; iniciativa int; 


