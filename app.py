from server.server import app, socketio
from routes.salas import salas_bp
from routes.fichas import fichas_bp
from routes.utils import utils_bp


app.secret_key = "alguma_chave_segura"

if __name__ == '__main__':
    app.register_blueprint(salas_bp)
    app.register_blueprint(fichas_bp)
    app.register_blueprint(utils_bp)
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
