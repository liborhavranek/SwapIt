from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Přihlašovací jméno nebo e-mail', validators=[DataRequired(message='Zadejte své přihlašovací jméno nebo e-mail.')])
    password = PasswordField('Heslo', validators=[DataRequired(message='Zadejte své heslo.')])
    submit = SubmitField('Přihlásit se')
