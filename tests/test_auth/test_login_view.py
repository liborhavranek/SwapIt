import time
import unittest

from flask import session
from flask_wtf.csrf import generate_csrf

from app import db, create_app
from tests.utils.get_csrf_token import get_csrf_token_from_response
from tests.utils.template_testing import captured_templates


class TestRegistrationViewTestCase(unittest.TestCase):

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

    def user_with_success_data(self, client, first_name='John', last_name='Doe', username='johndoe',
                               email='john.doe@example.com', password='password123',
                               confirm_password='password123'):
        response = client.get('/registration')
        csrf_token = get_csrf_token_from_response(response)
        return client.post('/registration', data={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'csrf_token': csrf_token
        }, follow_redirects=True)

    def test_login_status_code(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_template_count(self):
        with captured_templates(self.app) as templates:
            self.client.get('/login')
            self.assertEqual(len(templates), 1)

    def test_login_template_name(self):
        with captured_templates(self.app) as templates:
            self.client.get('/login')
            self.assertEqual(templates[0].name, 'auth_templates/login.html')

    def test_login_html_content(self):
        response = self.client.get('/login')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_login_mimetype(self):
        response = self.client.get('/login')
        self.assertEqual(response.mimetype, 'text/html')

    def test_loginform_have_200_response(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            c.get('/logout')
            login_response = c.post('/login', data={
                'username': 'johndoe',
                'password': 'password123',
                'csrf_token': self.get_csrf_token()
            }, follow_redirects=True)
            self.assertEqual(login_response.status_code, 200)

    def test_loginform_have_success_message_via_username(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            c.get('/logout')
            login_response = c.post('/login', data={
                'username': 'johndoe',
                'password': 'password123',
                'csrf_token': self.get_csrf_token()
            }, follow_redirects=True)
            expected_message = 'Přihlášení proběhlo úspěšně.'.encode('utf-8')
            self.assertIn(expected_message, login_response.data)

    def test_loginform_have_success_message_via_email(self):
        with self.client as c:
            self.user_with_success_data(c)
            c.get('/logout', follow_redirects=True)
            login_page_response = c.get('/login')
            csrf_token = get_csrf_token_from_response(login_page_response)
            login_response = c.post('/login', data={
                'username': 'john.doe@example.com',  # Použij 'username' místo 'email'
                'password': 'password123',
                'csrf_token': csrf_token  # Použij nový CSRF token
            }, follow_redirects=True)
            expected_message = 'Přihlášení proběhlo úspěšně.'.encode('utf-8')
            self.assertIn(expected_message, login_response.data)

    def test_loginform_have_wrong_username_message(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            c.get('/logout')
            login_response = c.post('/login', data={
                'username': 'wrongusername',
                'password': 'password123',
                'csrf_token': self.get_csrf_token()
            }, follow_redirects=True)
            expected_message = 'Nesprávné přihlašovací údaje nebo heslo.'.encode('utf-8')
            self.assertIn(expected_message, login_response.data)

    def test_loginform_have_wrong_password_message(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            c.get('/logout')
            login_response = c.post('/login', data={
                'username': 'johndoe',
                'password': 'wrongpassword',
                'csrf_token': self.get_csrf_token()
            }, follow_redirects=True)
            expected_message = 'Nesprávné přihlašovací údaje nebo heslo.'.encode('utf-8')
            self.assertIn(expected_message, login_response.data)


if __name__ == '__main__':
    unittest.main()
