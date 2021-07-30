from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from CustomDecorators import *
from models.commission import *

class Commission(Resource):
    @jwt_required()
    def get(self):
        com_data = [com.json() for com in CommissionModel.query.filter_by(
            vendor_id=get_jwt_identity())]
        return {"totalOrders": len(com_data), "Com_Details": com_data}, 200
    # @jwt_required()
    # def get(self):
    #     com_data = CommissionModel.query.filter_by(vendor_id=get_jwt_identity())
    #     print(com_data)
    #     if com_data:
    #         return {
    #             "Commission_Details": com_data.json()
    #         }, 200
    #     return {
    #         "No Vendor found..."
    #     }

class CommissionList(Resource):
    @jwt_required()
    def get(self):
        com_data= [com.json() for com in CommissionModel.query.all()]
        return {"totalData": len(com_data),"Commission": com_data}, 200
