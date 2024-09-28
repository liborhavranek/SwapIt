import unittest
import time
from app import app, db
from tests.utils.template_testing import captured_templates


class AppRoutesTestCase(unittest.TestCase):

    def setUp(self):
        time.sleep(0.1)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def test_test_page_status_code(self):
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)

    def test_test_page_template_count(self):
        with captured_templates(app) as templates:
            self.app.get('/test')
            self.assertEqual(len(templates), 1)

    def test_test_page_template_name(self):
        with captured_templates(app) as templates:
            self.app.get('/test')
            self.assertEqual(templates[0].name, 'base_templates/test.html')

    def test_test_page_html_content(self):
        response = self.app.get('/test')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_test_page_mimetype(self):
        response = self.app.get('/test')
        self.assertEqual(response.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
