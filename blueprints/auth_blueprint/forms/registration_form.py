from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from blueprints.auth_blueprint.validators.registration_form_validator import validate_first_name, validate_last_name, validate_username, validate_password, validate_email


class RegistrationForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired(), validate_first_name])
    last_name = StringField('Příjmení', validators=[DataRequired(), validate_last_name])
    username = StringField('Přihlašovací jméno', validators=[DataRequired(), validate_username])
    email = StringField('E-mailová adresa', validators=[DataRequired(), validate_email])
    password = PasswordField('Heslo', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Potvrzení hesla', validators=[DataRequired()])
    submit = SubmitField('Zaregistrovat se')
