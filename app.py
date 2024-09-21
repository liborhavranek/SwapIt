import os
import hashlib
from flask import Flask, session
from login import login_manager

from flask_socketio import SocketIO
from extensions import db, init_database
from blueprints_register import register_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['ADMIN_ACCESS_PASSWORD'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_database(app)

socketio = SocketIO(app)
register_blueprint(app)

login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha256(os.urandom(64)).hexdigest()
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    socketio.send('Message received: ' + msg)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created.")

    socketio.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)
