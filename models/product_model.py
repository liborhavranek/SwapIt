from datetime import datetime
from extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    swap_price = db.Column(db.Float, nullable=False)

    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=True)

    exchange_method = db.Column(db.String(50), nullable=False)
    delivery_option = db.Column(db.String(100), nullable=True)

    condition = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.String(50), nullable=False)

    desired_exchange = db.Column(db.Text, nullable=True)

    postal_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status = db.Column(db.String(50), nullable=False, default='available')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    images = db.relationship('Image', backref='product', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Product {self.title}>'

    def get_full_description(self):
        return f"{self.title} - {self.description}"
