from config import db
import datetime
from sqlalchemy import DateTime
from models import orders

class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30), unique=True, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    measure = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('CategoryModel', backref="category")


    def _init_(self, item_name, item_price, measure, category_id):
        self.item_name = item_name
        self.item_price = item_price
        self.measure = measure
        self.category_id = category_id

    def json(self):
        return {
            "Item_id": self.id,
            "Item_name": self.item_name,
            "Item_price": self.item_price,
            "measure": self.measure,
            "category_id": self.category_id,
            "Category": self.category.cat_name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_item_name(cls, item_name):
        return ItemModel.query.filter_by(item_name=item_name).first()

    @classmethod
    def find_by_id(cls, id):
        return ItemModel.query.filter_by(id=id).first()
