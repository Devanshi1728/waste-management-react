from config import db
import time
from datetime import datetime, date
from sqlalchemy import DateTime
from models import item;
from models import users;
from models import commission;

class OrderModel(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pickup_date = db.Column(
        db.String(50), nullable=False, default=datetime.utcnow)
    pickup_slot = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Pending")

    commission = db.relationship("CommissionModel", backref='order_com')
    user = db.relationship(
        "AuthModel", foreign_keys=[auth_id]) #ek min jo a
    vendor = db.relationship(
        "AuthModel", foreign_keys=[vendor_id])
    
    def __init__(self, auth_id, vendor_id,phone, address, pickup_date, pickup_slot, total):
        self.auth_id = auth_id
        self.vendor_id=vendor_id
        self.phone = phone
        self.address = address
        self.pickup_date = pickup_date
        self.pickup_slot = pickup_slot
        self.total = total

    def json(self):
        return {
            "order_id": self.order_id,
            "auth_id": self.auth_id,
            "Username" : self.user.username,
            "vendor_id": self.vendor_id,
            "Vendor": self.vendor.username,
            "Vendor_Phone": self.vendor.phone,
            "Phone": self.phone,
            "Address": self.address,
            "Pickup_Date": self.pickup_date,
            "Pickup_slot": self.pickup_slot,
            "Total": self.total,
            "Status":self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_orderid(cls, id):
        return OrderModel.query.filter_by(order_id=id).first()

    @classmethod
    def find_by_vendorid(cls, id):
        return OrderModel.query.filter_by(vendor_id=id).first()

class OrderDetailsModel(db.Model):
    __tablename__ = "orderDetails"
    OrderDetails_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    items = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    auth_id = db.Column(db.Integer)
    Order = db.relationship(
        "OrderModel", backref='order_detail')
    
    def __init__(self,OrderDetails_id,items, weight):
        self.OrderDetails_id = OrderDetails_id
        self.items = items
        self.weight = weight

    def json(self):
        return {
            "OrderDetails_id": self.OrderDetails_id,
            "Items": self.items,
            "Weight": self.weight,
            "auth_id": self.Order.auth_id,
            "Username": self.Order.user.username,
            "vendor_id": self.Order.vendor_id,
            "Vendor": self.Order.vendor.username,
            "Vendor_Phone": self.Order.vendor.phone,
            "Phone": self.Order.phone,
            "Address": self.Order.address,
            "Pickup_Date": self.Order.pickup_date,
            "Pickup_slot": self.Order.pickup_slot,
            "Total": self.Order.total,
            "Status": self.Order.status
        }
            
    @classmethod
    def find_by_orderDetailsid(cls, id):
        return OrderDetailsModel.query.filter_by(OrderDetails_id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


