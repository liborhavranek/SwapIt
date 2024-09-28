from datetime import datetime
import random
import string

from faker import Faker
from models.user_model import User

fake = Faker()


def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_user_with_defaults(**kwargs):
    defaults = {
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'user',
        'status': 'active',
        'date_of_birth': None,
        'gender': None,
        'profile_picture': None,
        'bio': None,
        'location': None,
        'phone_number': None,
        'website': None,
        'join_date': datetime.utcnow(),
        'last_login': None,
        'last_ip': None
    }
    defaults.update(kwargs)
    return defaults


def user_factory(**kwargs):
    user_data = create_user_with_defaults(**kwargs)
    return User(**user_data)


# Pomocné funkce pro specifické typy uživatelů, využívající `user_factory`
def create_admin_user(username='admin', email='admin@example.com', password='adminpass'):
    return user_factory(username=username, email=email, password=password, role='admin', first_name='Admin', last_name='User')


def create_regular_user(username='user', email='user@example.com', password='userpass'):
    return user_factory(username=username, email=email, password=password, role='user', first_name='Regular', last_name='User')


def create_manager_user(username='manager', email='editor@example.com', password='managerpass'):
    return user_factory(
        username=username,
        email=email,
        password=password,
        role='manager',
        first_name='Manager',
        last_name='User',
        gender='Non-binary',
        bio='Experienced content editor with a focus on quality and engagement.',
        location='New York',
        website='https://editor-profile.example.com'
    )


def create_full_profile_user(username='full_user', email='full@example.com', password='fullpass'):
    return user_factory(
        username=username,
        email=email,
        password=password,
        first_name='Full',
        last_name='Profile',
        role='admin',
        status='active',
        date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=45),
        gender='Female',
        profile_picture=fake.image_url(),
        bio='Senior developer with extensive experience in backend and frontend technologies.',
        location='San Francisco',
        phone_number='+1-555-0123',
        website='https://full-profile.example.com',
        join_date=datetime(2020, 5, 17),
        last_login=datetime(2024, 9, 1),
        last_ip='192.168.1.1'
    )
