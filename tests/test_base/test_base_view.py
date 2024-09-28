import unittest
from app import app
from tests.utils.page_class import TestViewCase
from tests.utils.template_testing import captured_templates


class TestHomepageViewTestCase(TestViewCase):

    def test_homepage_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_template_count(self):
        with captured_templates(app) as templates:
            self.app.get('/')
            self.assertEqual(len(templates), 1)

    def test_homepage_template_name(self):
        with captured_templates(app) as templates:
            self.app.get('/')
            self.assertEqual(templates[0].name, 'base_templates/base.html')

    def test_homepage_html_content(self):
        response = self.app.get('/')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_homepage_mimetype(self):
        response = self.app.get('/')
        self.assertEqual(response.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
