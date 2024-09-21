from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_database(app):
    db.init_app(app)
    from models.user_model import User
    from models.category_model import Category
    from models.brand_model import Brand
    with app.app_context():
        db.create_all()
        print("Database tables created.")
