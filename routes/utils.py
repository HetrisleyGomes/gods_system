from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file, g, flash
import psycopg2
import json

from controllers.ficha_controller import FichaController
from controllers.utils_controller import UtilsController
from controllers.mecha_controller import MechaController

from repositories.ficha_repository import FichaRepository
from repositories.utils_repository import UtilsRepository
from repositories.mecha_repository import MechaRepository


from config import db_connection_handler
from server.server import (
    socketio,
    app
)  # Importa socketio do módulo de configuração

utils_bp = Blueprint('utils', __name__)

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

# EQUIPAMENTOS ============================
@utils_bp.route('/equipamentos/<string:ficha_id>/')
def ficha_json_equipamentos(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)
    ficha = controller.get_ficha_tudo(ficha_id)

    erepository = UtilsRepository(connection)
    econtrollers = UtilsController(erepository)

    equipamentos = econtrollers.get_all_equipamentos()

    return render_template('equipamentos.html', ficha=ficha['body'], equipamentos=equipamentos['body'])

@utils_bp.route("/ficha/<string:ficha_id>/equipamentos", methods=["POST"])
def adicionar_equipamento_ficha(ficha_id):
    data = request.get_json()
    if not data or "equipamento_id" not in data:
        return jsonify({"error": "equipamento_id é obrigatório"}), 400

    equipamento_id = data["equipamento_id"]

    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    erepository = UtilsRepository(connection)
    econtrollers = UtilsController(erepository)

    try:
        econtrollers.set_ficha_equipamento(ficha_id, equipamento_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200

@utils_bp.route("/ficha/<string:ficha_id>/equipamentos/<int:equipamento_id>", methods=["DELETE"])
def remover_equipamento_ficha(ficha_id, equipamento_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    erepository = UtilsRepository(connection)
    econtrollers = UtilsController(erepository)
    try:
        econtrollers.remove_ficha_equipamento(ficha_id, equipamento_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200

@utils_bp.route("/ficha/<string:ficha_id>/equipamentos/json", methods=["GET"])
def listar_equipamentos_ficha(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    ficha_repository = FichaRepository(connection)
    equipamento_repository = UtilsRepository(connection)

    ficha_controller = FichaController(ficha_repository)
    equipamento_controller = UtilsController(equipamento_repository)

    try:
        ficha = ficha_controller.get_ficha_tudo(ficha_id)
        equipamentos = equipamento_controller.get_all_equipamentos()

        return jsonify({
            "ficha": ficha['body'],
            "equipamentos": equipamentos['body']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PODERES ============================
@utils_bp.route('/poderes/<string:ficha_id>/')
def ficha_json_poderes(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = FichaRepository(connection)
    controller = FichaController(repository)
    ficha = controller.get_ficha_tudo(ficha_id)

    prepository = UtilsRepository(connection)
    pcontrollers = UtilsController(prepository)

    poderes = pcontrollers.get_all_poderes()

    return render_template('poderes.html', ficha=ficha['body'], poderes=poderes['body'])

@utils_bp.route("/ficha/<string:ficha_id>/poderes", methods=["POST"])
def adicionar_poderes_ficha(ficha_id):
    data = request.get_json()
    if not data or "poder_id" not in data:
        return jsonify({"error": "poder_id é obrigatório"}), 400

    poder_id = data["poder_id"]

    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    prepository = UtilsRepository(connection)
    pcontrollers = UtilsController(prepository)

    try:
        pcontrollers.set_ficha_poder(ficha_id, poder_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200

@utils_bp.route("/ficha/<string:ficha_id>/poderes/<int:poder_id>", methods=["DELETE"])
def remover_poderes_ficha(ficha_id, poder_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    prepository = UtilsRepository(connection)
    pcontrollers = UtilsController(prepository)
    try:
        pcontrollers.remove_ficha_poder(ficha_id, poder_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ok"}), 200

@utils_bp.route("/ficha/<string:ficha_id>/poderes/json", methods=["GET"])
def listar_poderes_ficha(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    ficha_repository = FichaRepository(connection)
    poder_repository = UtilsRepository(connection)

    ficha_controller = FichaController(ficha_repository)
    poder_controller = UtilsController(poder_repository)

    try:
        ficha = ficha_controller.get_ficha_tudo(ficha_id)
        poderes = poder_controller.get_all_poderes()

        return jsonify({
            "ficha": ficha['body'],
            "poderes": poderes['body']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# MECHA ==========================
@utils_bp.route("/mecha/<string:ficha_id>/")
def mecha_router(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500

    repository = MechaRepository(connection)
    controller = MechaController(repository)

    mecha = controller.get_mecha_by_ficha_id(ficha_id)

    if mecha['status'] == 200:
        ficha_repository = FichaRepository(connection)
        ficha_controller = FichaController(ficha_repository)
        ficha = ficha_controller.get_ficha(ficha_id)
        return jsonify({"has_mecha": True, "mecha":mecha, "ficha":ficha})
    else:
        return jsonify({
            "has_mecha": False,
            "redirect_to": url_for("utils.criar_mecha", ficha_id=ficha_id)
        })

@utils_bp.route("/criar_mecha/<string:ficha_id>/")
def criar_mecha(ficha_id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    ficha_repository = FichaRepository(connection)
    ficha_controller = FichaController(ficha_repository)

    ficha = ficha_controller.get_ficha(ficha_id)
    
    return render_template("criar_mecha.html", ficha_id=ficha_id, ficha=ficha, is_editing=False)

@utils_bp.route("/form_criar_mecha", methods=["POST"])
def form_criar_mecha():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500

    repository = MechaRepository(connection)
    controller = MechaController(repository)

    if request.method == "POST":
        nome = request.form["nome"]
        ficha_id = request.form["ficha_id"]

        vida = request.form["vida"]
        armadura = request.form["armadura"]
        combate = request.form["combate"]
        pontaria = request.form["pontaria"]
        defesa = request.form["defesa"]
        forca = request.form["forca"]

        armas = json.loads(request.form.get("armas_json", "[]"))
        habilidades = json.loads(request.form.get("habilidades", "[]"))

    body = {
        "nome": nome,
        "ficha_id": ficha_id,
        "vida": vida,
        "armadura": armadura,
        "combate": combate,
        "pontaria": pontaria,
        "defesa": defesa,
        "forca": forca,
        "armas": armas,
        "habilidades": habilidades
    }

    resp = controller.set_mecha(body)

    return redirect(url_for("utils.ver_mecha", mecha_id=resp["body"]))

@utils_bp.route("/ficha/<int:id>/<int:valor>")
def alterar_vida_energia(id, valor):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = MechaRepository(connection)
    controller = MechaController(repository)

    controller.set_vida(id, valor)


    return { "body": True, "status": 200, }