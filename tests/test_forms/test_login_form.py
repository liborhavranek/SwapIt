import unittest
from blueprints.auth_blueprint.forms.login_form import LoginForm
from tests.utils.register_and_login_test_class import RegisterAndLoginTestCase


class LoginFormTestCase(RegisterAndLoginTestCase):

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
