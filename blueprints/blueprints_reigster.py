from flask import Blueprint
from blueprints.auth_blueprint.views import LoginView, RegistrationView, LogoutView
from blueprints.base_blueprint.views import BaseView, TestPageView, DashboardView


def register_routes(app):

    base_bp = Blueprint('base_bp', __name__)
    base_bp.add_url_rule('/', view_func=BaseView.as_view('index'))
    base_bp.add_url_rule('/test', view_func=TestPageView.as_view('test'))
    base_bp.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))

    auth_bp = Blueprint('auth_bp', __name__)
    auth_bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
    auth_bp.add_url_rule('/registration', view_func=RegistrationView.as_view('registration'))
    auth_bp.add_url_rule('/login', view_func=LoginView.as_view('login'))

    app.register_blueprint(base_bp)
    app.register_blueprint(auth_bp)
