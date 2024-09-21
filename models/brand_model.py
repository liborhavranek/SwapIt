from sqlalchemy.orm import relationship, backref
from extensions import db

class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=True)
    order = db.Column(db.Integer, default=0)
    visible = db.Column(db.Boolean, default=True)
    icon = db.Column(db.String(255), nullable=True)

    parent = relationship('Brand', remote_side=[id], backref=backref('subbrands', lazy='dynamic', cascade='all, delete-orphan', order_by="Brand.order"))