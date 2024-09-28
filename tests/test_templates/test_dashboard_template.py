import unittest
from tests.utils.register_and_login_test_class import BaseTestCase


class DashboardTemplateRenderingTestCase(BaseTestCase):

    def test_template_contains_doctype(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_template_contains_html_tag_with_language(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<html lang="cs">', response.data)

    def test_template_contains_head_tag(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<head>', response.data)

    def test_template_contains_body_tag(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<body>', response.data)

    def test_template_contains_closing_html_tag(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'</html>', response.data)


class DashboardTemplateImportsTestCase(BaseTestCase):

    def test_template_contains_charset_meta(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<meta charset="UTF-8">', response.data)

    def test_template_contains_viewport_meta(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<meta name="viewport"', response.data)

    def test_template_contains_title(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<title>SwapIt', response.data)

    def test_template_contains_bootstrap_css(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"',
                      response.data)

    def test_template_contains_bootstrap_js(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">',
                      response.data)

    def test_template_contains_bootstrap_icons(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"',
                      response.data)

    def test_template_contains_jquery(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>',
                      response.data)

    def test_template_contains_navbar_css(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<link rel="stylesheet" href="/static/css/navbar.css"',
                      response.data)

    def test_template_contains_sidebar_css(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<link rel="stylesheet" href="/static/css/sidebar.css"',
                      response.data)

    def test_template_contains_dashboard_css(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<link rel="stylesheet" href="/static/css/dashboard.css"',
                      response.data)

    def test_template_includes_nav_block(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<nav', response.data)

    def test_template_includes_navbar_brand(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'navbar-brand', response.data)

    def test_template_includes_sidebar_class(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'sidebar', response.data)

    def test_template_includes_message_js(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<script src="/static/js/message.js"></script>', response.data)

    def test_template_includes_drop_down_menu_js(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'<script src="/static/js/drop_down_menu.js"></script>', response.data)


class DashboardTemplateLinkTestCase(BaseTestCase):

    def test_dashboard_link_functionality(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

#   TODO: Uživatel musí být přihlášený aby test fungoval, až budeme testovat modely a zjistíme jak to udělat, tak to dopsat a přepsat test
#     def test_add_product_link_functionality(self):
#         response = self.client.get('/create_product')
#         self.assertEqual(response.status_code, 200)

    def test_add_product_link_present(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="/create_product" class="btn btn-swap mx-5">', html)

    def test_category_filter_link_functionality(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('data-bs-toggle="collapse" href="#category"', html)

    def test_category_filter_present(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('<div class="collapse" id="category">', html)

    def test_size_filter_link_functionality(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('data-bs-toggle="collapse" href="#size"', html)

    def test_color_filter_link_functionality(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('data-bs-toggle="collapse" href="#color"', html)

    def test_price_filter_link_functionality(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('data-bs-toggle="collapse" href="#price"', html)

    def test_rating_filter_link_functionality(self):
        response = self.client.get('/dashboard')
        html = response.data.decode('utf-8')
        self.assertIn('data-bs-toggle="collapse" href="#rating"', html)


if __name__ == '__main__':
    unittest.main()
