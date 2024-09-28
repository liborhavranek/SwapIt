from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class AdminLoginForm(FlaskForm):
    access_password = PasswordField('Heslo', validators=[DataRequired(message="Zadejte heslo.")])
    submit = SubmitField('Přihlásit se')
