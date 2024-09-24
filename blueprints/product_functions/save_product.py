from extensions import db
from models.product_model import Product


def save_product(form, category_id, user_id):
    new_product = Product(
        title=form.get('title'),
        description=form.get('description'),
        purchase_price=form.get('purchase_price'),
        swap_price=form.get('swap_price'),
        category=category_id,
        brand=form.get('brand'),
        exchange_method=form.get('exchange_method'),
        delivery_option=form.get('delivery_option'),
        desired_exchange=form.get('desired_exchange'),
        city=form.get('city'),
        postal_code=form.get('postal_code'),
        condition=form.get('condition'),
        availability=form.get('availability'),
        user_id=user_id
    )
    db.session.add(new_product)
    db.session.commit()
    return new_product
