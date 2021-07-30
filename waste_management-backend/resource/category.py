from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from CustomDecorators import *
from flask import jsonify, make_response
from models.category import CategoryModel
from models.item import ItemModel

class Category(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('cat_name', type=str, required=True)
    
    @admin_required
    def post(self):
        data = Category.parse.parse_args()
        category = CategoryModel.find_by_cat_name(data['cat_name'])
        if category:
            return {
                "CategoryAlreadyExistsError": {
                    "message": "Category with given name already exists"
                }}, 400
       
        category = CategoryModel(data['cat_name'])
        category.save_to_db()
        return {
            "message": "Category Create Successfully"
        }, 200


    def get(self, id):
        category = CategoryModel.find_by_cat_name(id)
        if category:
            return category.json()
        return {
            "CategoryNotFound": {
                "Category with given name already exists"
            }}, 400
    
    @admin_required
    def delete(self,id):
        # parse = reqparse.RequestParser()
        # data = parse.parse_args()
        category = CategoryModel.find_by_cat_id(id)
        if category:
            category.delete_from_db()
            return {
                "status": 200,
                "message": "Category Deleted"
            }
        return{
            "status": 404,
            "NotFoundError": "Category not Found.."
        }

    @admin_required
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('cat_name', type=str, required=True) 
        Category = CategoryModel.find_by_cat_id(id)
        if Category:
            data = parse.parse_args()
            Category.cat_name = data["cat_name"]
            Category.save_to_db()
            return {"updated": True, "data": Category.json()}, 200

class CategoryList(Resource):
    def get(self):
        cats = [category.json() for category in CategoryModel.query.all()]
        return {"TotalItems": len(cats), "Categories": cats,  "status": 'ok'}, 200
