from config import db
import datetime
from sqlalchemy import DateTime
from models import item;

class CategoryModel(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(30), unique=True, nullable=False)
    #creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    item = db.relationship('ItemModel', backref='itemCategory', lazy=True)

    def __init__(self, cat_name):
        self.cat_name = cat_name     
    
    def json(self):
        return {
            "Category_Id" : self.id,
            "Category_Name": self.cat_name       
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_cat_name(cls, cat_name):
        return CategoryModel.query.filter_by(cat_name=cat_name).first()

    @classmethod
    def find_by_cat_id(cls, id):
        return CategoryModel.query.filter_by(id=id).first()
        

