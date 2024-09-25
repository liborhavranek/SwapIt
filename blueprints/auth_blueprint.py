from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from blueprints.auth_function.registration_form_validation import validate_registration_form
from extensions import db
from models.user_model import User


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index_bp.dashboard'))

    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not csrf_token or csrf_token != session.get('_csrf_token'):
            abort(403)

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not validate_registration_form(username, email, password, confirm_password):
            return redirect(url_for('auth_bp.registration'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrace byla úspěšná. Nyní se můžete přihlásit.', 'success')
        return redirect(url_for('index_bp.dashboard'))

    return render_template('registration.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index_bp.dashboard'))
    if request.method == 'POST':
        login_input = request.form.get('username')
        password = request.form.get('password')
        if not login_input or not password:
            flash('Všechna pole musí být vyplněna.', 'danger')
            return redirect(url_for('auth_bp.login'))
        user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Přihlášení proběhlo úspěšně.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index_bp.dashboard'))
        else:
            flash('Nesprávné přihlašovací údaje nebo heslo.', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Byl jste úspěšně odhlášen.', 'success')
    return redirect(url_for('auth_bp.login'))
