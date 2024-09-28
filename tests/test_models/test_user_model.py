import time
import unittest
from datetime import datetime

from tests.factories.user_factory import create_admin_user, create_regular_user, create_manager_user

from sqlalchemy.exc import IntegrityError

from extensions import db
from app import create_app
from models.user_model import User


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        time.sleep(0.1)
        self.app, _ = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class AdminUserModelTestCase(UserModelTestCase):
    def setUp(self):
        super().setUp()
        before_creation = datetime.utcnow()
        admin_user = create_admin_user()
        db.session.add(admin_user)
        db.session.commit()
        self.saved_user = User.query.filter_by(username='admin').first()
        self.before_creation = before_creation
        self.after_creation = datetime.utcnow()

    def test_admin_user_created_successfully(self):
        self.assertIsNotNone(self.saved_user, "Admin uživatel nebyl uložen do databáze.")

    def test_admin_username_is_correct(self):
        self.assertEqual(self.saved_user.username, 'admin', "Uživatelské jméno se neshoduje.")

    def test_admin_email_is_correct(self):
        self.assertEqual(self.saved_user.email, 'admin@example.com', "E-mail se neshoduje.")

    def test_admin_password_is_correct(self):
        self.assertEqual(self.saved_user.password, 'adminpass', "Heslo se neshoduje.")

    def test_admin_first_name_is_correct(self):
        self.assertEqual(self.saved_user.first_name, 'Admin', "Křestní jméno se neshoduje.")

    def test_admin_last_name_is_correct(self):
        self.assertEqual(self.saved_user.last_name, 'User', "Příjmení se neshoduje.")

    def test_admin_role_is_correct(self):
        self.assertEqual(self.saved_user.role, 'admin', "Role uživatele se neshoduje.")

    def test_admin_status_is_correct(self):
        self.assertEqual(self.saved_user.status, 'active', "Status uživatele se neshoduje (výchozí hodnota).")

    def test_admin_date_of_birth_is_none(self):
        self.assertIsNone(self.saved_user.date_of_birth, "Datum narození by mělo být None.")

    def test_admin_gender_is_none(self):
        self.assertIsNone(self.saved_user.gender, "Pohlaví by mělo být None.")

    def test_admin_profile_picture_is_none(self):
        self.assertIsNone(self.saved_user.profile_picture, "Profilová fotka by měla být None.")

    def test_admin_bio_is_none(self):
        self.assertIsNone(self.saved_user.bio, "Bio by mělo být None.")

    def test_admin_location_is_none(self):
        self.assertIsNone(self.saved_user.location, "Lokace by měla být None.")

    def test_admin_phone_number_is_none(self):
        self.assertIsNone(self.saved_user.phone_number, "Telefonní číslo by mělo být None.")

    def test_admin_website_is_none(self):
        self.assertIsNone(self.saved_user.website, "Webová stránka by měla být None.")

    def test_admin_last_login_is_none(self):
        self.assertIsNone(self.saved_user.last_login, "Poslední přihlášení by mělo být None.")

    def test_admin_last_ip_is_none(self):
        self.assertIsNone(self.saved_user.last_ip, "Poslední IP adresa by měla být None.")

    def test_admin_join_date_is_not_none(self):
        self.assertIsNotNone(self.saved_user.join_date, "Datum připojení (`join_date`) je None, což je neočekávané.")

    def test_admin_join_date_is_correct(self):
        self.assertTrue(self.before_creation <= self.saved_user.join_date <= self.after_creation,
                        f"Datum připojení (`join_date`) {self.saved_user.join_date} není v očekávaném časovém intervalu mezi {self.before_creation} a {self.after_creation}.")


class RegularUserModelTestCase(UserModelTestCase):
    def setUp(self):
        super().setUp()
        before_creation = datetime.utcnow()
        regular_user = create_regular_user()
        db.session.add(regular_user)
        db.session.commit()
        self.saved_user = User.query.filter_by(username='user').first()
        self.before_creation = before_creation
        self.after_creation = datetime.utcnow()

    def test_regular_user_created_successfully(self):
        self.assertIsNotNone(self.saved_user, "Regular uživatel nebyl uložen do databáze.")

    def test_regular_username_is_correct(self):
        self.assertEqual(self.saved_user.username, 'user', "Uživatelské jméno se neshoduje.")

    def test_regular_email_is_correct(self):
        self.assertEqual(self.saved_user.email, 'user@example.com', "E-mail se neshoduje.")

    def test_regular_password_is_correct(self):
        self.assertEqual(self.saved_user.password, 'userpass', "Heslo se neshoduje.")

    def test_regular_first_name_is_correct(self):
        self.assertEqual(self.saved_user.first_name, 'Regular', "Křestní jméno se neshoduje.")

    def test_regular_last_name_is_correct(self):
        self.assertEqual(self.saved_user.last_name, 'User', "Příjmení se neshoduje.")

    def test_regular_role_is_correct(self):
        self.assertEqual(self.saved_user.role, 'user', "Role uživatele se neshoduje.")

    def test_regular_status_is_correct(self):
        self.assertEqual(self.saved_user.status, 'active', "Status uživatele se neshoduje (výchozí hodnota).")

    def test_regular_date_of_birth_is_none(self):
        self.assertIsNone(self.saved_user.date_of_birth, "Datum narození by mělo být None.")

    def test_regular_gender_is_none(self):
        self.assertIsNone(self.saved_user.gender, "Pohlaví by mělo být None.")

    def test_regular_profile_picture_is_none(self):
        self.assertIsNone(self.saved_user.profile_picture, "Profilová fotka by měla být None.")

    def test_regular_bio_is_none(self):
        self.assertIsNone(self.saved_user.bio, "Bio by mělo být None.")

    def test_regular_location_is_none(self):
        self.assertIsNone(self.saved_user.location, "Lokace by měla být None.")

    def test_regular_phone_number_is_none(self):
        self.assertIsNone(self.saved_user.phone_number, "Telefonní číslo by mělo být None.")

    def test_regular_website_is_none(self):
        self.assertIsNone(self.saved_user.website, "Webová stránka by měla být None.")

    def test_regular_last_login_is_none(self):
        self.assertIsNone(self.saved_user.last_login, "Poslední přihlášení by mělo být None.")

    def test_regular_last_ip_is_none(self):
        self.assertIsNone(self.saved_user.last_ip, "Poslední IP adresa by měla být None.")

    def test_regular_join_date_is_not_none(self):
        self.assertIsNotNone(self.saved_user.join_date, "Datum připojení (`join_date`) je None, což je neočekávané.")

    def test_regular_join_date_is_correct(self):
        self.assertTrue(self.before_creation <= self.saved_user.join_date <= self.after_creation,
                        f"Datum připojení (`join_date`) {self.saved_user.join_date} není v očekávaném časovém intervalu mezi {self.before_creation} a {self.after_creation}.")

    class ManagerUserModelTestCase(UserModelTestCase):
        def setUp(self):
            super().setUp()
            self.before_creation = datetime.utcnow()
            manager_user = create_manager_user()
            db.session.add(manager_user)
            db.session.commit()
            self.saved_user = User.query.filter_by(username='manager').first()
            self.after_creation = datetime.utcnow()

        def test_manager_user_created_successfully(self):
            self.assertIsNotNone(self.saved_user)

        def test_manager_username_is_correct(self):
            self.assertEqual(self.saved_user.username, 'manager')

        def test_manager_email_is_correct(self):
            self.assertEqual(self.saved_user.email, 'editor@example.com')

        def test_manager_password_is_correct(self):
            self.assertEqual(self.saved_user.password, 'managerpass')

        def test_manager_first_name_is_correct(self):
            self.assertEqual(self.saved_user.first_name, 'Manager')

        def test_manager_last_name_is_correct(self):
            self.assertEqual(self.saved_user.last_name, 'User')

        def test_manager_role_is_correct(self):
            self.assertEqual(self.saved_user.role, 'manager')

        def test_manager_status_is_correct(self):
            self.assertEqual(self.saved_user.status, 'active')

        def test_manager_date_of_birth_is_none(self):
            self.assertIsNone(self.saved_user.date_of_birth)

        def test_manager_gender_is_correct(self):
            self.assertEqual(self.saved_user.gender, 'Non-binary')

        def test_manager_profile_picture_is_none(self):
            self.assertIsNone(self.saved_user.profile_picture)

        def test_manager_bio_is_correct(self):
            self.assertEqual(self.saved_user.bio, 'Experienced content editor with a focus on quality and engagement.')

        def test_manager_location_is_correct(self):
            self.assertEqual(self.saved_user.location, 'New York')

        def test_manager_phone_number_is_none(self):
            self.assertIsNone(self.saved_user.phone_number)

        def test_manager_website_is_correct(self):
            self.assertEqual(self.saved_user.website, 'https://editor-profile.example.com')

        def test_manager_last_login_is_none(self):
            self.assertIsNone(self.saved_user.last_login)

        def test_manager_last_ip_is_none(self):
            self.assertIsNone(self.saved_user.last_ip)

        def test_manager_join_date_is_not_none(self):
            self.assertIsNotNone(self.saved_user.join_date)

        def test_manager_join_date_is_correct(self):
            self.assertTrue(self.before_creation <= self.saved_user.join_date <= self.after_creation)


class UserModelUniquesTestCase(UserModelTestCase):
    def setUp(self):
        super().setUp()
        self.before_creation = datetime.utcnow()
        manager_user = create_manager_user()
        db.session.add(manager_user)
        db.session.commit()
        self.after_creation = datetime.utcnow()

    def test_username_uniqueness_with_duplicate_username(self):
        user1 = User(username='testuser', email='test1@example.com', password='password', first_name='Test1',
                     last_name='User1')
        db.session.add(user1)
        db.session.commit()
        user2 = User(username='testuser', email='test2@example.com', password='password', first_name='Test2',
                     last_name='User2')
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_username_uniqueness_with_unique_username(self):
        user1 = User(username='uniqueuser1', email='unique1@example.com', password='password', first_name='Test1',
                     last_name='User1')
        user2 = User(username='uniqueuser2', email='unique2@example.com', password='password', first_name='Test2',
                     last_name='User2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.assertIsNotNone(User.query.filter_by(username='uniqueuser1').first())
        self.assertIsNotNone(User.query.filter_by(username='uniqueuser2').first())

    def test_email_uniqueness_with_duplicate_email(self):
        user1 = User(username='testuser1', email='testuser@example.com', password='password', first_name='Test1',
                     last_name='User1')
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='testuser2', email='testuser@example.com', password='password', first_name='Test2',
                     last_name='User2')
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_email_uniqueness_with_unique_email(self):
        user1 = User(username='user1', email='unique1@example.com', password='password', first_name='Test1',
                     last_name='User1')
        user2 = User(username='user2', email='unique2@example.com', password='password', first_name='Test2',
                     last_name='User2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.assertIsNotNone(User.query.filter_by(email='unique1@example.com').first())
        self.assertIsNotNone(User.query.filter_by(email='unique2@example.com').first())

    def test_repr_method(self):
        user = User(username='repruser', email='repr@example.com', password='password', first_name='Repr',
                    last_name='User')
        db.session.add(user)
        db.session.commit()
        expected_repr = '<User repruser>'
        self.assertEqual(repr(user), expected_repr)

    def test_user_without_required_fields_username(self):
        user = User(username=None, email='user@example.com', password='password', first_name='Test', last_name='User')
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_user_without_required_fields_email(self):
        user = User(username='testuser', email=None, password='password', first_name='Test', last_name='User')
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_user_without_required_fields_password(self):
        user = User(username='testuser', email='user@example.com', password=None, first_name='Test', last_name='User')
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_user_without_required_fields_first_name(self):
        user = User(username='testuser', email='user@example.com', password='password', first_name=None,
                    last_name='User')
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_user_without_required_fields_last_name(self):
        user = User(username='testuser', email='user@example.com', password='password', first_name='Test',
                    last_name=None)
        db.session.add(user)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_user_update_email(self):
        user = User(username='updateuser', email='oldemail@example.com', password='password', first_name='Test',
                    last_name='User')
        db.session.add(user)
        db.session.commit()

        user.email = 'newemail@example.com'
        db.session.commit()

        updated_user = User.query.filter_by(username='updateuser').first()
        self.assertEqual(updated_user.email, 'newemail@example.com')

    def test_user_deletion(self):
        user = User(username='deleteuser', email='deleteuser@example.com', password='password', first_name='Test',
                    last_name='User')
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        deleted_user = User.query.filter_by(username='deleteuser').first()
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()
