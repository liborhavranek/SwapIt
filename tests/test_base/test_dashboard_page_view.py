import unittest
from app import app
from tests.utils.page_class import TestViewCase
from tests.utils.template_testing import captured_templates


class TestDashboardViewTestCase(TestViewCase):

    def test_dashboard_status_code(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template_count(self):
        with captured_templates(app) as templates:
            self.app.get('/dashboard')
            self.assertEqual(len(templates), 1)

    def test_dashboard_template_name(self):
        with captured_templates(app) as templates:
            self.app.get('/dashboard')
            self.assertEqual(templates[0].name, 'dashboard.html')

    def test_dashboard_html_content(self):
        response = self.app.get('/dashboard')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_dashboard_mimetype(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
