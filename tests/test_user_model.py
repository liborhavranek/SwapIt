from datetime import datetime

import pytest
from models.user_model import User


def test_new_user(init_database):
    user = User(username='newuser', email='newuser@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='newuser').first()
    assert added_user is not None
    assert added_user.email == 'newuser@example.com'


def test_user_id(init_database):
    user = User(username='user_id_test', email='id_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_id_test').first()
    assert added_user.id is not None  # ID by mělo být automaticky generováno
    assert isinstance(added_user.id, int)  # ID by mělo být typu integer


def test_user_username(init_database):
    user = User(username='user_username_test', email='username_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(email='username_test@example.com').first()
    assert added_user.username == 'user_username_test'


def test_user_email(init_database):
    user = User(username='user_email_test', email='email_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_email_test').first()
    assert added_user.email == 'email_test@example.com'


def test_user_password(init_database):
    user = User(username='user_password_test', email='password_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_password_test').first()
    assert added_user.password == 'hashed_password'


def test_user_first_name(init_database):
    user = User(username='user_first_name_test', email='first_name_test@example.com', password='hashed_password', first_name='John')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_first_name_test').first()
    assert added_user.first_name == 'John'


def test_user_last_name(init_database):
    user = User(username='user_last_name_test', email='last_name_test@example.com', password='hashed_password',
                last_name='Doe')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_last_name_test').first()
    assert added_user.last_name == 'Doe'


def test_user_date_of_birth(init_database):
    user = User(username='user_dob_test', email='dob_test@example.com', password='hashed_password', date_of_birth=datetime(1990, 1, 1).date())
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_dob_test').first()
    assert added_user.date_of_birth == datetime(1990, 1, 1).date()


def test_user_profile_picture(init_database):
    user = User(username='user_profile_pic_test', email='profile_pic_test@example.com', password='hashed_password', profile_picture='http://example.com/pic.jpg')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_profile_pic_test').first()
    assert added_user.profile_picture == 'http://example.com/pic.jpg'


def test_user_bio(init_database):
    user = User(username='user_bio_test', email='bio_test@example.com', password='hashed_password', bio='This is a sample bio')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_bio_test').first()
    assert added_user.bio == 'This is a sample bio'


def test_user_location(init_database):
    user = User(username='user_location_test', email='location_test@example.com', password='hashed_password', location='Sample City')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_location_test').first()
    assert added_user.location == 'Sample City'


def test_user_phone_number(init_database):
    user = User(username='user_phone_test', email='phone_test@example.com', password='hashed_password', phone_number='+1234567890')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_phone_test').first()
    assert added_user.phone_number == '+1234567890'


def test_user_website(init_database):
    user = User(username='user_website_test', email='website_test@example.com', password='hashed_password', website='https://example.com')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_website_test').first()
    assert added_user.website == 'https://example.com'


def test_user_join_date(init_database):
    user = User(username='user_join_date_test', email='join_date_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_join_date_test').first()
    assert added_user.join_date is not None
    assert isinstance(added_user.join_date, datetime)


def test_user_last_login(init_database):
    user = User(username='user_last_login_test', email='last_login_test@example.com', password='hashed_password', last_login=datetime(2024, 1, 1, 10, 0))
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_last_login_test').first()
    assert added_user.last_login == datetime(2024, 1, 1, 10, 0)


def test_user_last_ip(init_database):
    user = User(username='user_last_ip_test', email='last_ip_test@example.com', password='hashed_password', last_ip='192.168.1.1')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_last_ip_test').first()
    assert added_user.last_ip == '192.168.1.1'


def test_user_status(init_database):
    user = User(username='user_status_test', email='status_test@example.com', password='hashed_password', status='inactive')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_status_test').first()
    assert added_user.status == 'inactive'


def test_user_repr(init_database):
    user = User(username='user_repr_test', email='repr_test@example.com', password='hashed_password')
    init_database.session.add(user)
    init_database.session.commit()

    added_user = User.query.filter_by(username='user_repr_test').first()
    assert repr(added_user) == '<User user_repr_test>'


def test_username_uniqueness(init_database):
    user1 = User(username='uniqueuser', email='user1@example.com', password='hashed_password')
    user2 = User(username='uniqueuser', email='user2@example.com', password='hashed_password')

    init_database.session.add(user1)
    init_database.session.commit()

    init_database.session.add(user2)
    with pytest.raises(Exception):  # Očekáváme chybu kvůli duplicitnímu username
        init_database.session.commit()


def test_email_uniqueness(init_database):
    user1 = User(username='user1', email='unique@example.com', password='hashed_password')
    user2 = User(username='user2', email='unique@example.com', password='hashed_password')

    init_database.session.add(user1)
    init_database.session.commit()

    init_database.session.add(user2)
    with pytest.raises(Exception):  # Očekáváme chybu kvůli duplicitnímu emailu
        init_database.session.commit()
