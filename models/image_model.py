from extensions import db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __repr__(self):
        return f'<Image {self.image_url} for Product ID {self.product_id}>'

    def is_assigned_to_product(self, product_id):
        return self.product_id == product_id
