import socketio
sio = socketio.Server()
app = socketio.WSGIApp(sio)