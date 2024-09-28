import unittest
import time
from flask import session
from flask_wtf.csrf import generate_csrf
from app import create_app, app
from extensions import db


class RegisterAndLoginTestCase(unittest.TestCase):
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


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        time.sleep(0.1)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
