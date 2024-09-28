import re
from wtforms import ValidationError
from models.user_model import User


def validate_username(form, field):
    username = field.data
    if not field.data:
        raise ValidationError(f'{field.label.text} je povinné pole.')
    if len(username) < 4:
        raise ValidationError('Přihlašovací jméno musí mít alespoň 4 znaky.')
    if len(username) > 50:
        raise ValidationError('Přihlašovací jméno nesmí přesáhnout 50 znaků.')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValidationError('Toto uživatelské jméno je již obsazeno. Zvolte jiné.')


def validate_email(form, field):
    email = field.data
    if not field.data:
        raise ValidationError(f'{field.label.text} je povinné pole.')
    if len(email) < 6:
        raise ValidationError('E-mailová adresa musí mít alespoň 5 znaků.')
    if len(email) > 100:
        raise ValidationError('E-mailová adresa nesmí mít více než 100 znaků.')
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        raise ValidationError('Zadejte platný formát e-mailové adresy.')
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        raise ValidationError('Tento e-mail je již zaregistrován. Použijte jiný nebo se přihlaste.')


def validate_password(form, field):
    password = form.password.data
    if not field.data:
        raise ValidationError(f'{field.label.text} je povinné pole.')
    confirm_password = form.confirm_password.data
    if len(password) < 4:
        raise ValidationError('Heslo musí mít alespoň 4 znaky.')
    if len(password) > 250:
        raise ValidationError('Heslo nemůže být delší než 250 znaků.')
    if password != confirm_password:
        raise ValidationError('Hesla se musí shodovat.')


def validate_first_name(form, field):
    first_name = form.first_name.data
    if not field.data:
        raise ValidationError(f'{field.label.text} je povinné pole.')
    if len(first_name) < 2:
        raise ValidationError('Jméno musí mít alespoň 2 znaky.')
    if len(first_name) > 50:
        raise ValidationError('Jméno nesmí přesáhnout 50 znaků.')


def validate_last_name(form, field):
    last_name = form.last_name.data
    if not field.data:
        raise ValidationError(f'{field.label.text} je povinné pole.')
    if len(last_name) < 2:
        raise ValidationError('Příjmení musí mít alespoň 2 znaky.')
    if len(last_name) > 50:
        raise ValidationError('Příjmení nesmí přesáhnout 50 znaků.')
