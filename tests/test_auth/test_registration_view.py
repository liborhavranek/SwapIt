import unittest
from models.user_model import User
from tests.utils.get_csrf_token import get_csrf_token_from_response
from tests.utils.register_and_login_test_class import RegisterAndLoginTestCase
from tests.utils.template_testing import captured_templates


class TestRegistrationViewTestCase(RegisterAndLoginTestCase):

    def user_with_success_data(self, client, **kwargs):
        response = client.get('/registration')
        csrf_token = get_csrf_token_from_response(response)
        data = {
            'first_name': kwargs.get('first_name', 'John'),
            'last_name': kwargs.get('last_name', 'Doe'),
            'username': kwargs.get('username', 'johndoe'),
            'email': kwargs.get('email', 'john.doe@example.com'),
            'password': kwargs.get('password', 'password123'),
            'confirm_password': kwargs.get('confirm_password', 'password123'),
            'csrf_token': csrf_token
        }
        return client.post('/registration', data=data, follow_redirects=True)

    def test_registration_status_code(self):
        response = self.client.get('/registration')
        self.assertEqual(response.status_code, 200)

    def test_registration_template_count(self):
        with captured_templates(self.app) as templates:
            self.client.get('/registration')
            self.assertEqual(len(templates), 1)

    def test_registration_template_name(self):
        with captured_templates(self.app) as templates:
            self.client.get('/registration')
            self.assertEqual(templates[0].name, 'auth_templates/registration.html')

    def test_registration_html_content(self):
        response = self.client.get('/registration')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_registration_mimetype(self):
        response = self.client.get('/registration')
        self.assertEqual(response.mimetype, 'text/html')

    def test_registration_form_submission_success_have_response_200(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            self.assertEqual(response.status_code, 200)

    def test_registration_form_submission_success_have_success_message(self):
        with self.client as c:
            response = self.user_with_success_data(c)
            expected_message = 'Registrace byla úspěšná. Nyní jste přihlášen/a.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_registration_form_submission_success_user_is_saved_in_db(self):
        with self.client as c:
            self.user_with_success_data(c)
            user = User.query.filter_by(username='johndoe').first()
            self.assertIsNotNone(user)

    def test_registration_first_name_too_short(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='A', last_name='Doe')
            expected_message = 'Jméno musí mít alespoň 2 znaky.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_registration_last_name_too_short(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='John', last_name='B')
            expected_message = 'Příjmení musí mít alespoň 2 znaky.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_registration_first_name_too_long(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='A' * 51, last_name='Doe')
            expected_message = 'Jméno nesmí přesáhnout 50 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_registration_last_name_too_long(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='John', last_name='B' * 51)
            expected_message = 'Příjmení nesmí přesáhnout 50 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_registration_first_name_valid(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='John', last_name='Doe')
            self.assertEqual(response.status_code, 200, "Validace pro správné jméno neměla vyhodit chybu.")

    def test_registration_last_name_valid(self):
        with self.client as c:
            response = self.user_with_success_data(c, first_name='John', last_name='Doe')
            self.assertEqual(response.status_code, 200, "Validace pro správné příjmení neměla vyhodit chybu.")


class TestRegistrationViewSecondTestCase(RegisterAndLoginTestCase):

    def user_with_success_data(self, client, **kwargs):
        response = client.get('/registration')
        csrf_token = get_csrf_token_from_response(response)
        data = {
            'first_name': kwargs.get('first_name', 'John'),
            'last_name': kwargs.get('last_name', 'Doe'),
            'username': kwargs.get('username', 'johndoe'),
            'email': kwargs.get('email', 'john.doe@example.com'),
            'password': kwargs.get('password', 'password123'),
            'confirm_password': kwargs.get('confirm_password', 'password123'),
            'csrf_token': csrf_token
        }
        return client.post('/registration', data=data, follow_redirects=True)

    def test_registration_form_submission_with_existing_username(self):
        with self.client as c:
            self.user_with_success_data(c, username='user')
            c.get('/logout')
            response = self.user_with_success_data(c, username='user')
            expected_message = 'Toto uživatelské jméno je již obsazeno.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_username_too_short(self):
        with self.client as c:
            response = self.user_with_success_data(c, username='abc')
            expected_message = 'Přihlašovací jméno musí mít alespoň 4 znaky.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_username_too_long(self):
        with self.client as c:
            response = self.user_with_success_data(c, username='a' * 51)
            expected_message = 'Přihlašovací jméno nesmí přesáhnout 50 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_email_too_short(self):
        with self.client as c:
            response = self.user_with_success_data(c, email='a@b.c')
            expected_message = 'E-mailová adresa musí mít alespoň 5 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_email_too_long(self):
        with self.client as c:
            long_email = 'a' * 95 + '@example.com'
            response = self.user_with_success_data(c, email=long_email)
            expected_message = 'E-mailová adresa nesmí mít více než 100 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_invalid_email_format(self):
        with self.client as c:
            invalid_emails = ['plainaddress', '@missingusername.com', 'username@.com', 'username@domain']
            for invalid_email in invalid_emails:
                response = self.user_with_success_data(c, email=invalid_email)
                expected_message = 'Zadejte platný formát e-mailové adresy.'.encode('utf-8')
                self.assertIn(expected_message, response.data, f"Chyba u neplatného e-mailu: {invalid_email}")

    def test_email_already_exists(self):
        with self.client as c:
            self.user_with_success_data(c, email='existing@example.com')
            c.get('/logout')
            response = self.user_with_success_data(c, email='existing@example.com')
            expected_message = 'Tento e-mail je již zaregistrován. Použijte jiný nebo se přihlaste.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_password_too_short(self):
        with self.client as c:
            response = self.user_with_success_data(c, password='123', confirm_password='123')
            expected_message = 'Heslo musí mít alespoň 4 znaky.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_password_too_long(self):
        with self.client as c:
            response = self.user_with_success_data(c, password='1'*251, confirm_password='1'*251)
            expected_message = 'Heslo nemůže být delší než 250 znaků.'.encode('utf-8')
            self.assertIn(expected_message, response.data)

    def test_passwords_do_not_match(self):
        with self.client as c:
            response = self.user_with_success_data(c, password='password123', confirm_password='differentpassword')
            expected_message = 'Hesla se musí shodovat.'.encode('utf-8')
            self.assertIn(expected_message, response.data)


if __name__ == '__main__':
    unittest.main()
