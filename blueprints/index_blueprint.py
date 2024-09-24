from flask import Blueprint, render_template, request

from blueprints.admin_blueprint import build_category_tree
from models.category_model import Category
from models.product_model import Product

index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/')
def index():
    return render_template('index.html')


@index_bp.route('/test')
def test():
    return render_template('test.html')


def get_category_ancestors(category):
    ancestors = []
    while category.parent:
        category = category.parent
        ancestors.insert(0, category)
    return ancestors


@index_bp.route('/dashboard', methods=['GET'])
def dashboard():
    products = Product.query.all()
    category_id = request.args.get('category_id', type=int)
    selected_category = None
    ancestor_ids = []

    categories = Category.query.all()
    categories_with_subcategories = build_category_tree(categories, include_invisible=True)

    if category_id:
        selected_category = Category.query.get_or_404(category_id)
        ancestors = get_category_ancestors(selected_category)
        ancestor_ids = [ancestor.id for ancestor in ancestors]
    else:
        ancestor_ids = []

    return render_template('dashboard.html',
                           categories=categories,
                           categories_tree=categories_with_subcategories,
                           selected_category=selected_category,
                           ancestor_ids=ancestor_ids,
                           products=products)




