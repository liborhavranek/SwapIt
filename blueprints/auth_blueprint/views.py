from flask import render_template, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user, login_required, logout_user
from blueprints.auth_blueprint.forms.registration_form import RegistrationForm
from blueprints.auth_blueprint.forms.login_form import LoginForm
from extensions import db
from blueprints.auth_blueprint.helpers.login_helpers import get_user_by_login_input, authenticate_user, perform_login
from blueprints.auth_blueprint.helpers.registration_helpers import create_user, save_user_to_db, handle_form_errors


class RegistrationView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('base_bp.dashboard'))
        form = RegistrationForm()
        return render_template('auth_templates/registration.html', form=form)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('base_bp.dashboard'))
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = create_user(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            save_user_to_db(new_user, db)
            return redirect(url_for('base_bp.dashboard'))
        handle_form_errors(form)
        return render_template('auth_templates/registration.html', form=form)


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('base_bp.dashboard'))
        form = LoginForm()
        return render_template('auth_templates/login.html', form=form)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('base_bp.dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = get_user_by_login_input(form.username.data)
            if authenticate_user(user, form.password.data):
                return perform_login(user)
            else:
                flash('Nesprávné přihlašovací údaje nebo heslo.', 'danger')
        return render_template('auth_templates/login.html', form=form)


class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        flash('Byl jste úspěšně odhlášen.', 'success')
        return redirect(url_for('auth_bp.login'))



