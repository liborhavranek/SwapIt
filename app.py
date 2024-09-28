import os
import hashlib
from flask import Flask, session
from login import login_manager

from flask_socketio import SocketIO
from extensions import db, init_database
from blueprints_register import register_blueprint
from blueprints.blueprints_reigster import register_routes


def create_app(testing=False, wtf_csrf_enabled=True):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config['ADMIN_ACCESS_PASSWORD'] = 'test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = wtf_csrf_enabled

    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    init_database(app)
    socketio = SocketIO(app)
    register_blueprint(app)
    register_routes(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    @socketio.on('message')
    def handle_message(msg):
        print('Received message: ' + msg)
        socketio.send('Message received: ' + msg)

    return app, socketio


app, socketio = create_app(testing=os.getenv('FLASK_ENV') == 'testing')

if __name__ == '__main__':
    if not app.config.get('TESTING'):
        with app.app_context():
            db.create_all()
            print("Database tables created.")
    socketio.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)
