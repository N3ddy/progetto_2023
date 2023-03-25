# Preparazione per la creazione dell'applicazione Flask
from flaskr import db, socketio
from flaskr.routes import app




if __name__ == '__main__':
    # Creazione delle tabelle
    with app.app_context():
        db.create_all()
    socketio.run(app, port=5000, host='192.168.1.11') 