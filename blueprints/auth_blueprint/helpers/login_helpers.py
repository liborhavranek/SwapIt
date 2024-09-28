from flask import flash, redirect, url_for, request
from flask_login import login_user
from werkzeug.security import check_password_hash
from models.user_model import User


def get_user_by_login_input(login_input):
    return User.query.filter((User.username == login_input) | (User.email == login_input)).first()


def authenticate_user(user, password):
    if user and check_password_hash(user.password, password):
        return True
    return False


def perform_login(user):
    login_user(user)
    next_page = request.args.get('next')
    flash('Přihlášení proběhlo úspěšně.', 'success')
    return redirect(next_page) if next_page else redirect(url_for('base_bp.dashboard'))
