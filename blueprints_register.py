from blueprints.index_blueprint import index_bp
from blueprints.auth_blueprint import auth_bp
from blueprints.admin_blueprint import admin_bp


def register_blueprint(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
