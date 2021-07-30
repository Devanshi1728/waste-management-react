from config import db
import datetime
from sqlalchemy import DateTime
from models import orders;
from sqlalchemy import and_


class AuthModel(db.Model):

    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), default="Customer")
    city = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    # orders = db.relationship('OrderModel', backref="user_order", lazy=True)

    def __init__(self, username, password, city, phone, role):
        self.username = username
        self.password = password
        self.city = city   
        self.role = role
        self.phone = phone

    def json(self):
        # json represantation of model object
        return {
            "UserId": self.id,
            "Username": self.username,
            "Password": self.password,
            "City": self.city,
            "Role":self.role,
            "Phone": self.phone
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return AuthModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return AuthModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_city(cls, city):
        return AuthModel.query.filter_by(city=city).first()

    @classmethod
    def find_by_role(cls, role):
        return AuthModel.query.filter_by(role=role).first()

    @classmethod
    def find_by_role_and_city(cls, role,city):
        return AuthModel.query.filter(and_(AuthModel.role == role, AuthModel.city == city)).first()

