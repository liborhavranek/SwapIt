import time
import unittest
from app import create_app
from extensions import db


class BaseTestCase(unittest.TestCase):
    """Základní třída pro nastavení aplikace a klienta pro testování."""

    def setUp(self):
        time.sleep(0.1)
        self.app, _ = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        time.sleep(0.1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class LoginTemplateRenderingTestCase(BaseTestCase):
    """Testy ověřující, že šablona login.html obsahuje základní HTML strukturu."""

    def test_template_contains_doctype(self):
        response = self.client.get('/login')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_template_contains_html_tag_with_language(self):
        response = self.client.get('/login')
        self.assertIn(b'<html lang="cs">', response.data)

    def test_template_contains_head_tag(self):
        response = self.client.get('/login')
        self.assertIn(b'<head>', response.data)

    def test_template_contains_body_tag(self):
        response = self.client.get('/login')
        self.assertIn(b'<body>', response.data)

    def test_template_contains_closing_html_tag(self):
        response = self.client.get('/login')
        self.assertIn(b'</html>', response.data)

    def test_template_contains_csrf_token(self):
        response = self.client.get('/login')
        self.assertIn(b'name="csrf_token"', response.data)


class LoginTemplateImportsTestCase(BaseTestCase):
    """Testy ověřující, že šablona login.html obsahuje správné importy a odkazy."""

    def test_template_contains_charset_meta(self):
        response = self.client.get('/login')
        self.assertIn(b'<meta charset="UTF-8">', response.data)

    def test_template_contains_viewport_meta(self):
        response = self.client.get('/login')
        self.assertIn(b'<meta name="viewport"', response.data)

    def test_template_contains_title(self):
        response = self.client.get('/login')
        self.assertIn(b'<title>SwapIt - Zaregistrujte se</title>', response.data)

    def test_template_contains_bootstrap_css(self):
        response = self.client.get('/login')
        self.assertIn(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap', response.data)

    def test_template_contains_custom_css(self):
        response = self.client.get('/login')
        self.assertIn(b'rel="stylesheet" href="/static/css/auth.css"', response.data)

    def test_template_contains_jquery(self):
        response = self.client.get('/login')
        self.assertIn(b'<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>', response.data)

    def test_template_contains_bootstrap_js(self):
        response = self.client.get('/login')
        self.assertIn(
            b'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>',
            response.data)


class LoginTemplateFormFieldsTestCase(BaseTestCase):
    """Testy ověřující, že šablona login.html obsahuje všechna pole formuláře."""

    def test_template_contains_username_field(self):
        response = self.client.get('/login')
        self.assertIn(b'name="username"', response.data)

    def test_template_contains_password_field(self):
        response = self.client.get('/login')
        self.assertIn(b'name="password"', response.data)

    def test_template_contains_submit_button(self):
        response = self.client.get('/login')
        expected_submit_button = '<input class="btn btn-primary" id="submit" name="submit" type="submit" value="Přihlásit se">'.encode('utf-8')
        self.assertIn(expected_submit_button, response.data)


class LoginTemplateLinkTestCase(BaseTestCase):

    def test_login_page_registration_link_functionality(self):
        response = self.client.get('/registration')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
