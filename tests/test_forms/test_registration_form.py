import unittest
from wtforms import ValidationError
from tests.utils.register_and_login_test_class import RegisterAndLoginTestCase
from extensions import db
from models.user_model import User
from blueprints.auth_blueprint.forms.registration_form import RegistrationForm


class RegistrationFormTestCase(RegisterAndLoginTestCase):

    def test_form_initializes_first_name_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.first_name.data, "Pole 'first_name' by mělo být inicializováno jako None.")

    def test_form_initializes_last_name_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.last_name.data, "Pole 'last_name' by mělo být inicializováno jako None.")

    def test_form_initializes_username_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.username.data, "Pole 'username' by mělo být inicializováno jako None.")

    def test_form_initializes_email_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.email.data, "Pole 'email' by mělo být inicializováno jako None.")

    def test_form_initializes_password_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.password.data, "Pole 'password' by mělo být inicializováno jako None.")

    def test_form_initializes_confirm_password_with_none(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(csrf_token=csrf_token)
            self.assertIsNone(form.confirm_password.data, "Pole 'confirm_password' by mělo být inicializováno jako None.")

    def test_form_populates_first_name_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(first_name='John', csrf_token=csrf_token)
            self.assertEqual(form.first_name.data, 'John', "Pole 'first_name' by mělo obsahovat hodnotu 'John'.")

    def test_form_populates_last_name_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(last_name='Doe', csrf_token=csrf_token)
            self.assertEqual(form.last_name.data, 'Doe', "Pole 'last_name' by mělo obsahovat hodnotu 'Doe'.")

    def test_form_populates_username_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='johndoe', csrf_token=csrf_token)
            self.assertEqual(form.username.data, 'johndoe', "Pole 'username' by mělo obsahovat hodnotu 'johndoe'.")

    def test_form_populates_email_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(email='john@example.com', csrf_token=csrf_token)
            self.assertEqual(form.email.data, 'john@example.com', "Pole 'email' by mělo obsahovat hodnotu 'john@example.com'.")

    def test_form_populates_password_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(password='password123', csrf_token=csrf_token)
            self.assertEqual(form.password.data, 'password123', "Pole 'password' by mělo obsahovat hodnotu 'password123'.")

    def test_form_populates_confirm_password_with_value(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(confirm_password='password123', csrf_token=csrf_token)
            self.assertEqual(form.confirm_password.data, 'password123', "Pole 'confirm_password' by mělo obsahovat hodnotu 'password123'.")

    def test_validate_username_unique_success_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='newuser', email='test@example.com', csrf_token=csrf_token)
            form.username.validators[1](form, form.username)

    def test_validate_username_unique_failure_with_csrf(self):
        existing_user = User(username='existinguser', email='test@example.com', password='password123', first_name='John', last_name='Do')
        db.session.add(existing_user)
        db.session.commit()
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='existinguser', email='test@example.com', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.username.validators[1](form, form.username)

    def test_validate_username_empty_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='', email='test@example.com', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.username.validators[1](form, form.username)

    def test_validate_username_length_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='new', email='test@example.com', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.username.validators[1](form, form.username)

    def test_validate_username_maximum_length_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='n'*51, email='test@example.com', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.username.validators[1](form, form.username)

    def test_validate_email_unique_success_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='newuser', email='new@example.com', csrf_token=csrf_token)
            form.email.validators[1](form, form.email)  # Neměla by vyvolat žádnou chybu

    def test_validate_email_unique_failure_with_csrf(self):
        existing_user = User(username='user', email='existing@example.com', password='password123', first_name='John', last_name='Do')
        db.session.add(existing_user)
        db.session.commit()
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='newuser', email='existing@example.com', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.email.validators[1](form, form.email)

    def test_validate_email_format_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            invalid_emails = ['plainaddress', 'missing@domain', 'missing.domain@', 'wrong@domain.']
            for email in invalid_emails:
                form = RegistrationForm(username='user', email=email, csrf_token=csrf_token)
                with self.assertRaises(ValidationError):
                    form.email.validators[1](form, form.email)

    def test_validate_email_empty_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='user', email='', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.email.validators[1](form, form.email)

    def test_validate_email_minimum_length_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            form = RegistrationForm(username='user', email='a@b.c', csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.email.validators[1](form, form.email)

    def test_validate_email_maximum_length_failure_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            long_email = 'a' * 91 + '@example.com'
            form = RegistrationForm(username='user', email=long_email, csrf_token=csrf_token)
            with self.assertRaises(ValidationError):
                form.email.validators[1](form, form.email)

    def test_validate_email_maximum_length_success_with_csrf(self):
        with self.app.test_request_context():
            csrf_token = self.get_csrf_token()
            valid_email = 'a' * 88 + '@example.com'
            form = RegistrationForm(username='user', email=valid_email, csrf_token=csrf_token)
            form.email.validators[1](form, form.email)

    def test_password_empty_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(password='', confirm_password='')
            with self.assertRaises(ValidationError):
                form.password.validators[1](form, form.password)

    def test_password_too_short_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(password='abc', confirm_password='abc')
            with self.assertRaises(ValidationError):
                form.password.validators[1](form, form.password)

    def test_password_minimum_length_success(self):
        with self.app.test_request_context():
            form = RegistrationForm(password='abcd', confirm_password='abcd')
            form.password.validators[1](form, form.password)

    def test_password_confirmation_mismatch_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(password='password123', confirm_password='password456')
            with self.assertRaises(ValidationError):
                form.password.validators[1](form, form.password)

    def test_password_confirmation_success(self):
        with self.app.test_request_context():
            form = RegistrationForm(password='password123', confirm_password='password123')
            form.password.validators[1](form, form.password)

    def test_first_name_empty_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='', last_name='Doe')
            with self.assertRaises(ValidationError):
                form.first_name.validators[1](form, form.first_name)

    def test_first_name_too_short_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='J', last_name='Doe')
            with self.assertRaises(ValidationError):
                form.first_name.validators[1](form, form.first_name)

    def test_first_name_minimum_length_success(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='Jo', last_name='Doe')
            form.first_name.validators[1](form, form.first_name)

    def test_first_name_too_long_failure(self):
        with self.app.test_request_context():
            long_name = 'J' * 51
            form = RegistrationForm(first_name=long_name, last_name='Doe')
            with self.assertRaises(ValidationError):
                form.first_name.validators[1](form, form.first_name)

    def test_first_name_maximum_length_success(self):
        with self.app.test_request_context():
            max_length_name = 'J' * 50
            form = RegistrationForm(first_name=max_length_name, last_name='Doe')
            form.first_name.validators[1](form, form.first_name)

    def test_last_name_empty_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='John', last_name='')
            with self.assertRaises(ValidationError):
                form.last_name.validators[1](form, form.last_name)

    def test_last_name_too_short_failure(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='John', last_name='D')
            with self.assertRaises(ValidationError):
                form.last_name.validators[1](form, form.last_name)

    def test_last_name_minimum_length_success(self):
        with self.app.test_request_context():
            form = RegistrationForm(first_name='John', last_name='Do')
            form.last_name.validators[1](form, form.last_name)

    def test_last_name_too_long_failure(self):
        with self.app.test_request_context():
            long_last_name = 'D' * 51
            form = RegistrationForm(first_name='John', last_name=long_last_name)
            with self.assertRaises(ValidationError):
                form.last_name.validators[1](form, form.last_name)

    def test_last_name_maximum_length_success(self):
        with self.app.test_request_context():
            max_length_last_name = 'D' * 50
            form = RegistrationForm(first_name='John', last_name=max_length_last_name)
            form.last_name.validators[1](form, form.last_name)


if __name__ == '__main__':
    unittest.main()
