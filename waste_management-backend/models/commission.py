from config import db
import time
from datetime import datetime, date
from sqlalchemy import DateTime
from models import item;
from models import users;

class CommissionModel(db.Model):
    __tablename__ = "commission"
    commission_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    amount = db.Column(db.Float(precision='3,2'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    total_amt = db.Column(db.Integer)
    date = db.Column(
        db.String(50), nullable=False, default=datetime.utcnow)

    vendor = db.relationship(
        "AuthModel", foreign_keys=[vendor_id])
    
    def __init__(self, amount):     
        self.amount = amount

    def json(self):
        return {
            "Commission_id": self.commission_id,
            "Order_id": self.order_id,
            "Total_Amount": self.total_amt,
            "Commission_Amount": self.amount,
            "Vendor_id": self.vendor_id,
            "Vendor": self.vendor.username,
            "Date": self.date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_comid(cls, id):
        return CommissionModel.query.filter_by(commission_id=id).first()

    @classmethod
    def find_by_orderid(cls, id):
        return CommissionModel.query.filter_by(order_id=id).first()
