from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
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

        # Validace prázdných polí
        if not username or not email or not password or not confirm_password:
            flash('Všechna pole musí být vyplněna.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Validace délky username
        if len(password) < 4:
            flash('Přihlašovací jméno musí mít alespoň 4 znaků.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Kontrola, zda hesla souhlasí
        if password != confirm_password:
            flash('Hesla se neshodují.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Validace délky hesla
        if len(password) < 4:
            flash('Heslo musí mít alespoň 4 znaků.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Validace formátu e-mailu
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            flash('Zadejte platný formát e-mailové adresy.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Kontrola, zda uživatelské jméno již existuje
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Toto uživatelské jméno je již obsazeno. Zvolte jiné.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Kontrola, zda e-mail již existuje
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Tento e-mail je již zaregistrován. Použijte jiný nebo se přihlaste.', 'danger')
            return redirect(url_for('auth_bp.registration'))

        # Vytvoření nového uživatele
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
