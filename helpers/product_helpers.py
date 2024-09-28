from models.product_model import Product


def get_all_products():
    return Product.query.all()
