import os
from flask import Flask
from flask_socketio import SocketIO
from login import login_manager
from extensions import db, init_database
from blueprints_register import register_blueprint
from blueprints.blueprints_reigster import register_routes


def create_app(testing=False, wtf_csrf_enabled=True):
    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'secret!'
    flask_app.config['ADMIN_ACCESS_PASSWORD'] = 'test'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['WTF_CSRF_ENABLED'] = wtf_csrf_enabled

    if testing:
        flask_app.config['TESTING'] = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # Inicializace rozšíření
    init_database(flask_app)
    socketio_instance = SocketIO(flask_app)
    register_blueprint(flask_app)
    register_routes(flask_app)
    login_manager.init_app(flask_app)
    login_manager.login_view = 'auth_bp.login'

    @socketio_instance.on('message')
    def handle_message(msg):
        print('Received message: ' + msg)
        socketio_instance.send('Message received: ' + msg)

    return flask_app, socketio_instance


app, socketio = create_app(testing=os.getenv('FLASK_ENV') == 'testing')

if __name__ == '__main__':
    if not app.config.get('TESTING'):
        with app.app_context():
            db.create_all()
            print("Database tables created.")
    socketio.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)
