import unittest
import time
from app import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        time.sleep(0.1)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()


class BaseTemplateRenderingTestCase(BaseTestCase):

    def test_template_contains_doctype(self):
        response = self.client.get('/')
        self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_template_contains_html_tag_with_language(self):
        response = self.client.get('/')
        self.assertIn(b'<html lang="cs">', response.data)

    def test_template_contains_head_tag(self):
        response = self.client.get('/')
        self.assertIn(b'<head>', response.data)

    def test_template_contains_body_tag(self):
        response = self.client.get('/')
        self.assertIn(b'<body>', response.data)

    def test_template_contains_footer_tag(self):
        response = self.client.get('/')
        self.assertIn(b'<footer>', response.data)

    def test_template_contains_closing_html_tag(self):
        response = self.client.get('/')
        self.assertIn(b'</html>', response.data)


class BaseTemplateImportsTestCase(BaseTestCase):

    def test_template_contains_charset_meta(self):
        response = self.client.get('/')
        self.assertIn(b'<meta charset="UTF-8">', response.data)

    def test_template_contains_viewport_meta(self):
        response = self.client.get('/')
        self.assertIn(b'<meta name="viewport"', response.data)

    # Testování title stránky
    def test_template_contains_title(self):
        response = self.client.get('/')
        self.assertIn(b'<title>SwapIt', response.data)

    def test_template_contains_bootstrap_css(self):
        response = self.client.get('/')
        self.assertIn(b'<link href="https://cdn.jsdelivr.net/npm/bootstrap',
                      response.data)

    def test_template_contains_custom_css(self):
        response = self.client.get('/')
        self.assertIn(b'rel="stylesheet" href="/static/css/styles.css"',
                      response.data)

    def test_template_contains_bootstrap_js(self):
        response = self.client.get('/')
        self.assertIn(
            b'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>',
            response.data)


class BaseTemplateLinkTestCase(BaseTestCase):

    def test_dashboard_link_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="/dashboard" class="btn btn-primary">Začít Swapovat</a>', html)

    def test_dashboard_link_functionality(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_how_it_works_anchor_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="#how-it-works-section" class="btn btn-outline-light">Jak to funguje</a>', html)

    def test_how_it_works_anchor_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup_link_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="#" class="btn btn-primary">Zaregistrovat se</a>', html)

    def test_signup_link_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_faq_collapse_one_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn(
            '<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne"',
            html)

    def test_faq_collapse_one_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_faq_collapse_two_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn(
            '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo"',
            html)

    def test_faq_collapse_two_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_faq_collapse_three_present(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn(
            '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree"',
            html)

    def test_faq_collapse_three_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class BaseTemplateContentTestCase(BaseTestCase):

    def test_template_contains_main_heading_h1(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<h1 class="swap-text">', html)

    def test_template_contains_swap_green_span(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<span class="swap-green">Swap</span>', html)

    def test_template_contains_it_black_span(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<span class="it-black">It</span>', html)

    def test_template_contains_start_swap_button(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="/dashboard" class="btn btn-primary">Začít Swapovat</a>', html)

    # Testování přítomnosti tlačítka "Jak to funguje"
    def test_template_contains_how_it_works_button(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<a href="#how-it-works-section" class="btn btn-outline-light">Jak to funguje</a>', html)

    def test_template_contains_how_it_works_section(self):
        response = self.client.get('/')
        self.assertIn(b'<h2>Jak to funguje</h2>', response.data)

    def test_template_how_it_works_register_step(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Zaregistrujte se', html)

    def test_template_how_it_works_upload_item_step(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Nahrajte předmět', html)

    def test_template_how_it_works_find_item_step(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Najděte, co chcete', html)

    def test_template_how_it_works_swap_item_step(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Vyměňte', html)

    def test_template_contains_why_swap_section(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<h2>Proč swapovat?</h2>', html)

    def test_template_contains_benefit_save_money(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Ušetříte peníze', html)

    def test_template_contains_benefit_save_planet(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Šetříte planetu', html)

    def test_template_contains_benefit_get_what_you_want(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Získáte co chcete', html)

    def test_template_contains_popular_categories_section(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<h2>Nejoblíbenější kategorie</h2>', html)

    def test_template_contains_user_reviews_section(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('<h2>Co říkají naši uživatelé</h2>', html)

    def test_template_contains_review_jana_novakova(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Jana Nováková', html)

    def test_template_contains_review_petr_svoboda(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Petr Svoboda', html)

    def test_template_contains_review_eva_mala(self):
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('Eva Malá', html)


if __name__ == '__main__':
    unittest.main()
