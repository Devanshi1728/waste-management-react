from functools import wraps
from flask import Flask
from models.users import AuthModel
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request

from app_init import app, jwt

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims["role"] == "Admin":
            return fn(*args, **kwargs)
        elif claims['role'] == "Vendor":
            return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != "Admin":
            return {"message": "Only Admin has this right !!"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def vendor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] != "Vendor":
            return {"message": "Vendors only"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    urole = AuthModel.find_by_id(identity)
    print("urole = ", urole.role)
    if urole.role == 'Admin':
        return {'role': 'Admin'}
    elif urole.role == 'Vendor':
        return {'role' :'Vendor'}
    else:
        return { 'role' : 'Customer'}
    
