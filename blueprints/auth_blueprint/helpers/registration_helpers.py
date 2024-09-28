from flask import flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from models.user_model import User


def create_user(first_name, last_name, username, email, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=hashed_password
    )
    return new_user


def save_user_to_db(user, db):
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash('Registrace byla úspěšná. Nyní jste přihlášen/a.', 'success')


def handle_form_errors(form):
    for _field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}', 'danger')
