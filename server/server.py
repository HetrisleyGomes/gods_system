from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins=["*"])

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("update_request")
def handle_update_request(data):
    # Broadcast update to all clients
    emit("update", data, broadcast=True)

@socketio.on("message")
def handle_message(data):
    print("received message: " + data)

@socketio.on("status_update")
def handle_status_update(data):
    # Broadcast para todos
    emit("status_sync", data, broadcast=True)

@socketio.on("join_sala")
def join_sala(data):
    join_room(data["sala_id"])

@socketio.on("leave_sala")
def leave_sala(data):
    leave_room(data["sala_id"])