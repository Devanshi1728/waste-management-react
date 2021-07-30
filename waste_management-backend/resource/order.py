from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from CustomDecorators import *
from models.orders import *
from models.commission import *


class Order(Resource):
    @jwt_required()
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, required=True)
        parse.add_argument('phone', type=str, required=True)
        parse.add_argument('address', type=str, required=True)
        parse.add_argument('items', type=str)
        parse.add_argument('pickup_date', type=str, required=True)
        parse.add_argument('pickup_slot', type=str, required=True)

        data = parse.parse_args()
        user = AuthModel.find_by_username(data['username'])
        #print("Vendo r vedor = ", user)

        #order = OrderModel.find_by_
        vendor = AuthModel.find_by_role_and_city("Vendor", user.city)
        #print(vendor)
        auth_id = user.id

        vendor_id = vendor.id
        city = user.city
        weight = 0
        total = 0

        if vendor and user:
            order = OrderModel(
                auth_id, vendor_id, data['phone'], data['address'], data['pickup_date'], data['pickup_slot'], total)
            #print("order  = ", order)
            order.save_to_db()
            order_id = order.order_id
            OrderDetails = OrderDetailsModel(order_id, data['items'], weight)
            OrderDetails.save_to_db()
            return {
                "message": "Order Added Successfully",
                "Order": order.json()
            }, 200
        return {
            "message": "Vendor is not available"
        }, 500

    @vendor_required
    def get(self):
        orders = [order.json() for order in OrderModel.query.filter_by(
            vendor_id=get_jwt_identity())]
        return {"totalOrders": len(orders), "Orders": orders}, 200


class UserOrder(Resource):
    @jwt_required()
    def get(self):
        orders = [order.json() for order in OrderModel.query.filter_by(
            auth_id=get_jwt_identity(), status="Pending")]
        orderdetail = [orderDetail.json() for orderDetail in OrderDetailsModel.query.filter_by(
            auth_id=get_jwt_identity())]
        #print("order dertails = ",orderdetail)
        return {"totalOrders": len(orderdetail), 'orders':orders, 'orderdetail': orderdetail}, 200


class OrderList(Resource):
    @admin_required
    def get(self):
        orders = [order.json() for order in OrderModel.query.all()]
        return {"totalOrders": len(orders), "Orders": orders}, 200

class OrderDetails(Resource):
    @jwt_required()
    def get(self, id):
        order_details = OrderDetailsModel.find_by_orderDetailsid(id)
        if order_details:
            return {
                "Order_Details": order_details.json()
            }, 200
        return {
            "message": "No Order Data"
        }, 400

    @vendor_required
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('weight', type=str)
        parse.add_argument('total', type=int)
        parse.add_argument('amount', type=float)
        parse.add_argument('vendor_id', type=int)

        data = parse.parse_args()
        order_details = OrderDetailsModel.find_by_orderDetailsid(id)
        order = OrderModel.find_by_orderid(id)
        com = CommissionModel(data['amount'])

        # print("order = ", order)
        # print("order id = ", order.order_id)
        # print("AUTH id = ", order.auth_id)
        # print("com = ", com)

        if order_details:
            data = parse.parse_args()

            order_details.weight = data['weight']
            order_details.auth_id = order.auth_id

            order.total = data['total']
            order.status = "Completed"

            com.total_amt = data['total']
            com.order_id = order.order_id
            com.vendor_id = order.vendor_id
            com.amount = data['amount']
            com.date = order.pickup_date

            order_details.save_to_db()
            order.save_to_db()
            com.save_to_db()
            return {"updated": True, "data": order_details.json(), "order": order.json(), "Commission": com.json()}, 200
