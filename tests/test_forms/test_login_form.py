import time
import unittest
from flask import session
from flask_wtf.csrf import generate_csrf

from app import create_app
from extensions import db
from blueprints.auth_blueprint.forms.login_form import LoginForm


class LoginFormTestCase(unittest.TestCase):
    def setUp(self):
        time.sleep(0.1)
        self.app, _ = create_app(testing=True, wtf_csrf_enabled=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_csrf_token(self):
        with self.app.test_request_context():
            csrf_token = generate_csrf()
            session['csrf_token'] = csrf_token
            return csrf_token

    def test_form_initializes_username_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = LoginForm(csrf_token=csrf_token)
            self.assertIsNone(form.username.data)

    def test_form_initializes_password_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = LoginForm(csrf_token=csrf_token)
            self.assertIsNone(form.password.data)

    def test_form_populates_username_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = LoginForm(username='testuser', csrf_token=csrf_token)
            self.assertEqual(form.username.data, 'testuser')

    def test_form_populates_password_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = LoginForm(password='testpassword', csrf_token=csrf_token)
            self.assertEqual(form.password.data, 'testpassword',)


if __name__ == '__main__':
    unittest.main()
