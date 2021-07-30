from flask import Flask
from flask_restful import Api

from flask_migrate import Migrate
from resource.users import Registration, User, UserLogin, UserLogout, Vendor, UserPwd, UserRegistration
from resource.category import *
from resource.item import *
from resource.order import *
from resource.commission import *

from app_init import app,api,jwt
blocklist = set()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@app.before_first_request
def init():
    db.create_all()

# @jwt.token_in_blocklist_loader
# def check_if_token_in_blocklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in blocklist
#     # return models.RevokedTokenModel.is_jti_blocklisted(jti)


# @jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token["jti"]
#     return jti in blacklist

api.add_resource(Registration, '/auth/registration')
api.add_resource(UserRegistration, '/auth/user/registration')
api.add_resource(UserLogin, '/auth/login', '/user')
api.add_resource(UserLogout, '/logout')

api.add_resource(UserPwd, '/user/profile/<int:id>')
api.add_resource(User, '/delete', '/userlist', '/users/<int:id>')
api.add_resource(Vendor, '/vendorlist')

api.add_resource(Category, '/category', '/category/<int:id>')
api.add_resource(CategoryList, '/catlist')

api.add_resource(Item, '/item','/item/<int:id>') #post, get, put
api.add_resource(ItemList, '/itemlist') #get

api.add_resource(Order, '/order', '/order/<int:id>') #post, get
api.add_resource(OrderDetails, '/order_details/<int:id>')  #get #put
api.add_resource(OrderList, '/orderlist')  #admin order list
api.add_resource(UserOrder, '/user/orderdetail') #user order list

api.add_resource(Commission, '/com') #get 
api.add_resource(CommissionList, '/commission')  #getlist

migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)

if __name__ == '__main__':
    from config import db 
    app.run(port=5000, debug=True)
