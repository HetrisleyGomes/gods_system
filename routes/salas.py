from flask import render_template, url_for, request, redirect, Blueprint, jsonify, send_file, g, flash, session
from flask_login import login_user, logout_user, login_required
import psycopg2

from controllers.sala_controller import SalaController
from controllers.ficha_controller import FichaController

from repositories.ficha_repository import FichaRepository
from repositories.sala_repository import SalaRepository

from config import db_connection_handler
from server.server import (
    emit,
    socketio,
    app
)  # Importa socketio do módulo de configuração

salas_bp = Blueprint('salas', __name__)

SALA_LOGS = {}

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


@salas_bp.route('/')
def main():
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = SalaRepository(connection)
    controller = SalaController(repository)
    salas_request = controller.get_salas()
    salas = []
    if salas_request['status'] == 200:
        salas = salas_request['body']

    return render_template("main.html", salas = salas)


@salas_bp.route('/criar_sala')
def criar_sala():
    return render_template("criar_sala.html")

@salas_bp.route('/form_sala', methods=["GET", "POST"])
def form_sala():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        senha = request.form["senha"].strip()
        codigo = request.form["codigo"].strip()

        # validação extra no backend (sempre bom conferir)
        if len(nome) > 50 or len(senha) > 50 or len(codigo) != 5:
            flash("Dados inválidos. Verifique os campos.")
            return redirect("/criar_sala")

        connection = get_db_connection()
        if connection is None:
            flash("Problemas em conectar ao banco")
            return "Erro ao conectar ao banco de dados.", 500
        
        repository = SalaRepository(connection)
        controller = SalaController(repository)

        body = {'nome': nome, 'senha': senha, 'codigo': codigo}
        response = controller.create(body)
        if response['status'] == 200:
            flash("Sala criada com sucesso!")
            return redirect(f"/sala/{response['body']}")
        
    return redirect(url_for('salas.main'))

@salas_bp.route('/sala/<id>')
def sala_view(id):
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = SalaRepository(connection)
    controller = SalaController(repository)
    sala_request = controller.get_sala(id)

    frepository = FichaRepository(connection)
    fcontroller = FichaController(frepository)
    
    fichas_request = fcontroller.get_fichas_por_sala(id)

    if sala_request['status'] == 200:
        sala = sala_request['body']
    
    if fichas_request['status'] == 200:
        fichas = fichas_request['body']
    else:
        fichas = []

    return render_template('sala.html', sala=sala, fichas=fichas)

@salas_bp.route("/sala/<string:sala_id>/mestre/status")
def status_mestre(sala_id):
    is_mestre = session.get(f"mestre_sala_{sala_id}", False)

    return jsonify({
        "is_mestre": is_mestre
    })

@salas_bp.route("/sala/<string:sala_id>/mestre/login", methods=["POST"])
def login_mestre(sala_id):
    # Obtem o form
    data = request.json
    senha = data.get("senha")

    # Obtem informações da sala
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = SalaRepository(connection)
    controller = SalaController(repository)
    sala_request = controller.get_sala(sala_id)

    SENHA_SALA = sala_request['body']['senha']

    # Verifica senha
    if senha != SENHA_SALA:
        return jsonify({"success": False}), 401

    session[f"mestre_sala_{sala_id}"] = True

    return jsonify({"success": True})

@salas_bp.route("/sala/<string:sala_id>/mestre/notes")
def get_notes_mestre(sala_id):
    if not session.get(f"mestre_sala_{sala_id}"):
        return jsonify({"error": "Não autorizado"}), 403

    # Obtem informações da sala
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    repository = SalaRepository(connection)
    controller = SalaController(repository)
    notes = controller.get_notes(sala_id)

    return jsonify({
        "id": sala_id,
        "notes": notes['body'][0]
    })

@salas_bp.route("/sala/<string:sala_id>/get_fichas")
def get_fichas_sala(sala_id):
    # Obtem informações da sala
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500
    
    frepository = FichaRepository(connection)
    fcontroller = FichaController(frepository)
    
    fichas_request = fcontroller.get_fichas_por_sala(sala_id)
    
    if fichas_request['status'] == 200:
        fichas = fichas_request['body']
    else:
        fichas = []

    return jsonify(
        fichas
    )

@salas_bp.route("/sala/<string:sala_id>/mestre/notes-update", methods=["POST"])
def update_notes_mestre(sala_id):
    if not session.get(f"mestre_sala_{sala_id}"):
        return jsonify({"error": "Não autorizado"}), 403

    # Obtem form
    data = request.get_json()
    if not data or "notes" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    notas = data["notes"]

    if not isinstance(notas, str):
        return jsonify({"error": "Formato inválido de notas"}), 400

    # Obtem informações da sala
    connection = get_db_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500

    try:
        repository = SalaRepository(connection)
        controller = SalaController(repository)
        resp = controller.set_notes(sala_id, notas)

        if not resp:
            return jsonify({"error": "Sala não encontrada"}), 404

        return jsonify({
            "id": sala_id,
            "notes": notas
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@salas_bp.route("/sala/<string:sala_id>/logs")
def get_logs(sala_id):
    return jsonify({
        "logs": SALA_LOGS.get(sala_id, [])
    })

@socketio.on("log")
def handle_log(data):
    sala_id = data["sala_id"]
    log = data["log"]

    if sala_id not in SALA_LOGS:
        SALA_LOGS[sala_id] = []

    SALA_LOGS[sala_id].append(log)

    if len(SALA_LOGS[sala_id]) > 30:
        SALA_LOGS[sala_id].pop(0)

    emit("log_sync", {"log": log}, room=sala_id)
