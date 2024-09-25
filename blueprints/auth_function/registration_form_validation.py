import re
from flask import flash
from models.user_model import User


def validate_registration_form(username, email, password, confirm_password):
    if not username or not email or not password or not confirm_password:
        flash('Všechna pole musí být vyplněna.', 'danger')
        return False
    if len(username) < 4:
        flash('Přihlašovací jméno musí mít alespoň 4 znaky.', 'danger')
        return False
    if password != confirm_password:
        flash('Hesla se neshodují.', 'danger')
        return False
    if len(password) < 4:
        flash('Heslo musí mít alespoň 4 znaky.', 'danger')
        return False
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        flash('Zadejte platný formát e-mailové adresy.', 'danger')
        return False
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Toto uživatelské jméno je již obsazeno. Zvolte jiné.', 'danger')
        return False
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        flash('Tento e-mail je již zaregistrován. Použijte jiný nebo se přihlaste.', 'danger')
        return False
    return True
