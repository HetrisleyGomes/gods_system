const socket = io();

// Enviar algo para o servidor
function enviarLog(mensagem) {
    socket.emit("message", mensagem);
}
