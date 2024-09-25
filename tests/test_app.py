import sys
import unittest
from unittest.mock import patch

from app import app, db, generate_csrf_token


class AppConfigTestCase(unittest.TestCase):
    """Testy pro konfiguraci aplikace."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_db_is_imported(self):
        from app import db
        self.assertIsNotNone(db, "Databáze nebyla importována.")

    def test_init_database_is_imported(self):
        from app import init_database
        self.assertIsNotNone(init_database, "Funkce init_database nebyla importována.")

    def test_register_blueprint_is_imported(self):
        from app import register_blueprint
        self.assertIsNotNone(register_blueprint, "Funkce register_blueprint nebyla importována.")

    def test_secret_key_configuration(self):
        self.assertEqual(app.config['SECRET_KEY'], 'test_secret_key')

    def test_admin_access_password_configuration(self):
        self.assertEqual(app.config['ADMIN_ACCESS_PASSWORD'], 'test')

    def test_sqlalchemy_database_uri_configuration(self):
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

    def test_sqlalchemy_track_modifications_configuration(self):
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    @patch('extensions.init_database')
    def test_init_database_called(self, mock_init_database):
        if 'app' in sys.modules:
            del sys.modules['app']
        import app
        mock_init_database.assert_called_once_with(app.app)

    @patch('flask_socketio.SocketIO')
    def test_socketio_initialization(self, mock_socketio):
        if 'app' in sys.modules:
            del sys.modules['app']
        import app
        mock_socketio.assert_called_once_with(app.app)

    @patch('login.login_manager')
    def test_login_manager_init_app(self, mock_login_manager):
        if 'app' in sys.modules:
            del sys.modules['app']
        import app
        mock_login_manager.init_app.assert_called_once_with(app.app)

    @patch('login.login_manager')
    def test_login_view_set_correctly(self, mock_login_manager):
        if 'app' in sys.modules:
            del sys.modules['app']
        import app
        self.assertEqual(mock_login_manager.login_view, 'auth_bp.login')

    def test_generate_csrf_token_returns_existing_token(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['_csrf_token'] = 'existing_token'
            response = client.get('/')
            with client.session_transaction() as session:
                self.assertEqual(session['_csrf_token'], 'existing_token')

    def test_csrf_token_registered_as_jinja_global_key(self):
        with app.app_context():
            self.assertIn('csrf_token', app.jinja_env.globals)

    def test_csrf_token_registered_as_jinja_global_value(self):
        with app.app_context():
            self.assertEqual(app.jinja_env.globals['csrf_token'], generate_csrf_token)

    @patch('flask.Flask.register_blueprint')
    def test_register_index_blueprint(self, mock_register_blueprint):
        from app import register_blueprint
        from blueprints.index_blueprint import index_bp
        register_blueprint(app)
        mock_register_blueprint.assert_any_call(index_bp)

    @patch('flask.Flask.register_blueprint')
    def test_register_auth_blueprint(self, mock_register_blueprint):
        from app import register_blueprint
        from blueprints.auth_blueprint import auth_bp
        register_blueprint(app)
        mock_register_blueprint.assert_any_call(auth_bp)

    @patch('flask.Flask.register_blueprint')
    def test_register_admin_blueprint(self, mock_register_blueprint):
        from app import register_blueprint
        from blueprints.admin_blueprint import admin_bp
        register_blueprint(app)
        mock_register_blueprint.assert_any_call(admin_bp)

    @patch('flask.Flask.register_blueprint')
    def test_register_add_product_blueprint(self, mock_register_blueprint):
        from app import register_blueprint
        from blueprints.add_product_blueprint import add_product_bp
        register_blueprint(app)
        mock_register_blueprint.assert_any_call(add_product_bp)

# TODO tyto tři testy přesunout k testování login testovat pro každou šablonu, kde je csrf_token
    def test_no_csrf_token_in_session_initially(self):
        with self.app as client:
            with client.session_transaction() as session:
                self.assertNotIn('_csrf_token', session)

    def test_csrf_token_generated_on_request(self):
        with self.app as client:
            client.get('/login')
            with client.session_transaction() as session:
                self.assertIn('_csrf_token', session)

    def test_csrf_token_length(self):
        with self.app as client:
            client.get('/login')
            with client.session_transaction() as session:
                self.assertEqual(len(session['_csrf_token']), 64)


if __name__ == '__main__':
    unittest.main()
