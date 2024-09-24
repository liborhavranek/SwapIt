from blueprints.product_functions.save_product import save_product
from extensions import db
from models.brand_model import Brand
from models.category_model import Category
from flask_login import login_required, current_user
from blueprints.product_functions.process_image import process_images
from blueprints.product_functions.product_validation import validate_product_form
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

add_product_bp = Blueprint('add_product_bp', __name__)


@add_product_bp.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        form = request.form
        images = request.files.getlist('images')
        errors, category_id = validate_product_form(form, images)
        if errors:
            for error in errors:
                flash(error, 'danger')
            form_data = form.to_dict()
            return render_template('user/create_product.html', categories=Category.query.filter_by(parent_id=None).all(),
                                   brands=Brand.query.all(), form_data=form_data)
        try:
            new_product = save_product(form, category_id, current_user.id)
            process_images(images, new_product.id)
            flash('Produkt byl úspěšně přidán!', 'success')
            return redirect(url_for('index_bp.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Nastala chyba: {str(e)}', 'danger')
            form_data = form.to_dict()
            return render_template('user/create_product.html', categories=Category.query.filter_by(parent_id=None).all(),
                                   brands=Brand.query.all(), form_data=form_data)
    else:
        main_categories = Category.query.filter_by(parent_id=None).all()
        brands = Brand.query.all()
        form_data = {}
        return render_template('user/create_product.html', categories=main_categories, brands=brands, form_data=form_data)


@add_product_bp.route('/get_subcategories/<int:category_id>', methods=['GET'])
@login_required
def get_subcategories(category_id):
    subcategories = Category.query.filter_by(parent_id=category_id).all()
    subcategories_data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    return jsonify(subcategories=subcategories_data)
