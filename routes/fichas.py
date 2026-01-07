from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file, g, flash
import psycopg2
import json

from controllers.sala_controller import SalaController
from controllers.ficha_controller import FichaController
from controllers.utils_controller import UtilsController


from repositories.ficha_repository import FichaRepository
from repositories.sala_repository import SalaRepository
from repositories.utils_repository import UtilsRepository


from config import db_connection_handler
from server.server import (
    socketio,
    app
)  # Importa socketio do módulo de configuração

fichas_bp = Blueprint('fichas', __name__)

# Função para conectar ao banco de dados
def get_db_connection():
    if 'db_conn' not in g:
        try:
            conn_string = db_connection_handler.get_connection_string()
            g.db_conn = psycopg2.connect(conn_string)
            print("Conexão ao banco PostgreSQL estabelecida para a requisição.")
        except Exception as e:
            print(f"Erro ao conectar no banco: {e}")
            g.db_conn = None
    return g.db_conn

# Função para fechar a conexão no final de cada requisição
@app.teardown_appcontext
def close_db_connection(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
        print("Conexão com o banco fechada.")

@fichas_bp.route('/criar_ficha/<sala_id>')
def criar_ficha(sala_id):
    bonus_construtores = 5
    return render_template('criar_ficha.html', sala_id=sala_id, bonus_construtores=bonus_construtores)

@fichas_bp.route('/form_criar_ficha', methods=["GET", "POST"])
def form_criar_ficha():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)

    urepository = UtilsRepository(connection)
    ucontroller = UtilsController(urepository)

    # Pega os dados do form
    sala_id = request.form.get("sala_id")
    nome = request.form.get("nome_personagem")
    cor = request.form.get("cor")
    especie = request.form.get("especie")
    arquetipo = request.form.get("arquetipo")

    # ATRIBUTO
    atributos_json = request.form.get("atributos_json")
    atributos = json.loads(atributos_json)

    ficha = {
        "id": None,
        "sala_id": sala_id,
        "nome_personagem": nome,
        "vida": atributos["vida"],
        "energia": atributos["energia"],
        "armadura": atributos["armadura"],
        "nivel": 1,
        "xp": 0,
        "cor": cor,
        "especie": especie,
        "arquetipo": arquetipo,
        "forca": atributos["forca"],
        "constituicao": atributos["constituicao"],
        "inteligencia": atributos["inteligencia"],
        "destreza": atributos["destreza"],
        "carisma": atributos["carisma"],
        "combate": atributos["combate"],
        "atletismo": atributos["atletismo"],
        "tecnologia": atributos["tecnologia"],
        "percepcao": atributos["percepcao"],
        "conhecimento": atributos["conhecimento"],
        "pontaria": atributos["pontaria"],
        "furtividade": atributos["furtividade"],
        "atuacao": atributos["atuacao"],
        "iniciativa": atributos["iniciativa"],
    }

    response = controller.create(ficha)
    id_ficha = response['body']
    poderes_by_arquetipo = return_poderes_id_by_arquetipo(arquetipo)

    for poder_id in poderes_by_arquetipo:
        ucontroller.set_ficha_poder(id_ficha, poder_id)

    especie_poderes = return_poderes_by_especie(especie)
    for poder_id in especie_poderes:
        ucontroller.set_ficha_poder(id_ficha, poder_id)

    ucontroller.set_ficha_poder(id_ficha, return_poderes_by_cor(cor))
    return redirect(f"/sala/{sala_id}")

@fichas_bp.route('/ficha/<string:ficha_id>/json')
def ficha_json(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)
    ficha = controller.get_ficha_tudo(ficha_id)

    return jsonify(ficha)

@fichas_bp.route("/ficha/<string:id>/<int:type>/<int:valor>")
def alterar_vida_energia(id, type, valor):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)
    if type == 1:
        controller.set_vida(id, valor)
    elif type == 0:
        controller.set_energia(id, valor)

    return { "body": True, "status": 200, }

@fichas_bp.route("/ficha/editar/<string:id>")
def editar_ficha(id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)
    response = controller.get_ficha(id)
    if response['status'] == 200:
        ficha = response['body']
    else:
        ficha = {}

    return render_template('edit_ficha.html', ficha=ficha, id=id)

@fichas_bp.route('/form_editar_ficha', methods=["GET", "POST"])
def form_editar_ficha():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)

    # Pega os dados do form
    ficha_id = request.form.get("ficha_id")
    sala_id = request.form.get("sala_id")
    nome = request.form.get("nome_personagem")
    cor = request.form.get("cor")
    vida = request.form.get("vida")
    energia = request.form.get("energia")
    armadura = request.form.get("armadura")
    nivel = request.form.get("nivel")
    xp = request.form.get("xp")
    especie = request.form.get("especie")
    arquetipo = request.form.get("arquetipo")
    forca = request.form.get("forca")
    constituicao = request.form.get("constituicao")
    inteligencia = request.form.get("inteligencia")
    destreza = request.form.get("destreza")
    carisma = request.form.get("carisma")
    combate = request.form.get("combate")
    atletismo = request.form.get("atletismo")
    tecnologia = request.form.get("tecnologia")
    percepcao = request.form.get("percepcao")
    conhecimento = request.form.get("conhecimento")
    pontaria = request.form.get("pontaria")
    furtividade = request.form.get("furtividade")
    atuacao = request.form.get("atuacao")
    iniciativa = request.form.get("iniciativa")
    vida_atual = request.form.get("vida_atual")
    energia_atual = request.form.get("energia_atual")

    ficha = {
        "id": ficha_id,
        "sala_id": sala_id,
        "nome_personagem": nome,
        "vida": vida,
        "energia": energia,
        "armadura": armadura,
        "nivel": nivel,
        "xp": xp,
        "cor": cor,
        "especie": especie,
        "arquetipo": arquetipo,
        "forca": forca,
        "constituicao": constituicao,
        "inteligencia": inteligencia,
        "destreza": destreza,
        "carisma": carisma,
        "combate": combate,
        "atletismo": atletismo,
        "tecnologia": tecnologia,
        "percepcao": percepcao,
        "conhecimento": conhecimento,
        "pontaria": pontaria,
        "furtividade": furtividade,
        "atuacao": atuacao,
        "iniciativa": iniciativa,
        "vida_atual": vida_atual,
        "energia_atual": energia_atual,
    }
    response = controller.edit_ficha(ficha_id, ficha)
    return redirect(f"/sala/{sala_id}")


def return_poderes_id_by_arquetipo(arquetipo):
    match arquetipo:
        case "combatente":
            return [73, 56, 54]
        case "genio":
            return [76, 97, 58]
        case "celere":
            return [100, 62, 34]
        case "guardiao":
            return [59, 63, 64]
        case "peregrino":
            return [71, 81, 76]
        case "sobrevivente":
            return [30, 32, 54]
        case "atirador":
            return [43, 35, 41]
        case "vanguarda":
            return [96, 72, 32]
        case "a_sombra":
            return [88, 72, 54]

def return_poderes_by_especie(especie):
    match especie:
        case "humano":
            return [1, 2, 3]
        case "sphynx":
            return [4, 5]
        case "sirians":
            return [6, 7, 8]
        case "android":
            return [9, 10, 11]
        case "aquitiano":
            return [12, 13, 14]
        case "sauriano":
            return [15, 16]
        case "rafkan":
            return [17, 18, 19]

def return_poderes_by_cor(cor):
    match cor:
        case "vermelho":
            return 20
        case "azul":
            return 21
        case "amarelo":
            return 23
        case "rosa":
            return 24
        case "verde":
            return 22
        case "preto":
            return 25
        case "branco":
            return 26