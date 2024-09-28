from extensions import db
from datetime import datetime
from flask_login import UserMixin
from models.user_role import Role


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Definice všech sloupců
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

    def __init__(self, username, email, password, first_name=None, last_name=None, role=Role.ADMIN, status='active',
                 date_of_birth=None, gender=None, profile_picture=None, bio=None, location=None,
                 phone_number=None, website=None, join_date=None, last_login=None, last_ip=None):

        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.status = status
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.profile_picture = profile_picture
        self.bio = bio
        self.location = location
        self.phone_number = phone_number
        self.website = website
        self.join_date = join_date if join_date else datetime.utcnow()
        self.last_login = last_login
        self.last_ip = last_ip

    def __repr__(self):
        return f'<User {self.username}>'
