from sqlalchemy.orm import relationship, backref
from extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    order = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(255), nullable=True)

    parent = relationship('Category', remote_side=[id], backref=backref('subcategories', lazy='dynamic', cascade='all, delete-orphan', order_by="Category.order"))

    def get_all_subcategories(self):
        return Category.query.filter_by(parent_id=self.id).order_by(Category.order).all()

    @staticmethod
    def get_root_categories():
        return Category.query.filter_by(parent_id=None).order_by(Category.order).all()

    def __repr__(self):
        return f'<Category {self.name}>'
