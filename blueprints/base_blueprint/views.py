from flask import render_template, request, Response
from flask.views import MethodView
from helpers.product_helpers import get_all_products
from helpers.category_helpers import get_all_categories, get_selected_category_and_ancestors
from blueprints.admin_blueprint import build_category_tree


class BaseView(MethodView):
    def get(self) -> Response:
        html = render_template('base_templates/base.html')
        return Response(html, status=200, mimetype='text/html')


class TestPageView(MethodView):
    def get(self) -> Response:
        html = render_template('base_templates/test.html')
        return Response(html, status=200, mimetype='text/html')


class DashboardView(MethodView):
    def get(self):
        products = get_all_products()
        categories = get_all_categories()
        category_id = request.args.get('category_id', type=int)
        categories_with_subcategories = build_category_tree(categories, include_invisible=True)
        selected_category, ancestor_ids = get_selected_category_and_ancestors(category_id)
        return render_template('dashboard.html',
                               categories=categories,
                               categories_tree=categories_with_subcategories,
                               selected_category=selected_category,
                               ancestor_ids=ancestor_ids,
                               products=products)
