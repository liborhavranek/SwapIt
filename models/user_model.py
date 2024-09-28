from datetime import datetime
from flask_login import UserMixin
from extensions import db
from models.user_role import Role


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=Role.ADMIN)
    status = db.Column(db.String(20), default='active')
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    last_ip = db.Column(db.String(45), nullable=True)

    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.password = password
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return f'<User {self.username}>'
