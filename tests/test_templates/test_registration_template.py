import time
import unittest
from app import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        time.sleep(0.1)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()


class RegistrationTemplateRenderingTestCase(BaseTestCase):
    """Testy ověřující, že šablona registration.html obsahuje základní HTML strukturu."""

    def test_template_contains_doctype(self):
        response = self.client.get('/registration')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_template_contains_html_tag_with_language(self):
        response = self.client.get('/registration')
        self.assertIn(b'<html lang="cs">', response.data)

    def test_template_contains_head_tag(self):
        response = self.client.get('/registration')
        self.assertIn(b'<head>', response.data)

    def test_template_contains_body_tag(self):
        response = self.client.get('/registration')
        self.assertIn(b'<body>', response.data)

    def test_template_contains_closing_html_tag(self):
        response = self.client.get('/registration')
        self.assertIn(b'</html>', response.data)

    def test_template_contains_csrf_token(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="csrf_token"', response.data)


class RegistrationTemplateImportsTestCase(BaseTestCase):

    def test_template_contains_charset_meta(self):
        response = self.client.get('/registration')
        self.assertIn(b'<meta charset="UTF-8">', response.data)

    def test_template_contains_viewport_meta(self):
        response = self.client.get('/registration')
        self.assertIn(b'<meta name="viewport"', response.data)

    def test_template_contains_title(self):
        response = self.client.get('/registration')
        self.assertIn(b'<title>SwapIt - Zaregistrujte se</title>', response.data)

    def test_template_contains_bootstrap_css(self):
        response = self.client.get('/registration')
        self.assertIn(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap', response.data)

    def test_template_contains_custom_css(self):
        response = self.client.get('/registration')
        self.assertIn(b'rel="stylesheet" href="/static/css/auth.css"', response.data)

    def test_template_contains_jquery(self):
        response = self.client.get('/registration')
        self.assertIn(b'<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>', response.data)

    def test_template_contains_bootstrap_js(self):
        response = self.client.get('/registration')
        self.assertIn(b'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>', response.data)

    def test_template_contains_message_js(self):
        response = self.client.get('/registration')
        self.assertIn(b'<script src="/static/js/message.js"></script>', response.data)


class RegistrationTemplateFormFieldsTestCase(BaseTestCase):
    """Testy ověřující, že šablona registration.html obsahuje všechna pole formuláře."""

    def test_template_contains_first_name_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="first_name"', response.data)

    def test_template_contains_last_name_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="last_name"', response.data)

    def test_template_contains_username_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="username"', response.data)

    def test_template_contains_email_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="email"', response.data)

    def test_template_contains_password_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="password"', response.data)

    def test_template_contains_confirm_password_field(self):
        response = self.client.get('/registration')
        self.assertIn(b'name="confirm_password"', response.data)

    def test_template_contains_submit_button(self):
        response = self.client.get('/registration')
        self.assertIn(b'<input class="btn btn-primary" id="submit" name="submit" type="submit" value="Zaregistrovat se">', response.data)


if __name__ == '__main__':
    unittest.main()
