import datetime as dt
import json

from werkzeug.exceptions import BadRequest, NotFound
from flask_restful import Resource, reqparse
from flask import request

from app.api.v2.helpers.token import TokenGen
from app.api.v2.models.orders import OrderModels
from app.api.v2.helpers.helpers import auth_required, check_admin
from app.api.v2.helpers.serializer import Serializers

serialize = Serializers()
order_models = OrderModels()
token_gen = TokenGen()

class AdminOrders(Resource):
    """ This will handle admin related functions on orders as a whole """
    @check_admin
    def get(self):
        orders_result = order_models.get_orders()
        orders = []
        if orders_result:
            for u in orders_result:
                order = serialize.serialize_order(u)
                orders.append(order)
            return (
                {
                    "message":"Success",
                    "orders":orders
                }
            ), 200
        else: 
            return BadRequest("No order table")
            

class OrdersMain(Resource):
    """ This class holds the endpoints for orders as a whole """
    @auth_required
    def get(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
            raise NotFound("Token absences please ")

        user_id = token_gen.decode_auth_token(auth_token)
        orders_result = order_models.find_order_by_user_id(user_id)
        orders = []
        if orders_result:
            for u in orders_result:
                order = serialize.serialize_order(u)
                orders.append(order)

        return (
            {
                "status":"Success",
                "orders":orders
            }
        ), 200
      
    @auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meal',
            type=str,
            required=True,
            help="An order must have a meal"
        )
        parser.add_argument(
            'qty',
            type=int,
            required=True,
            help="Let us know the meal quantity"
        )
        parser.add_argument(
            'price',
            type=int,
            required=True,
            help="A meal must have a price"
        )
        parser.add_argument(
            'description',
            type=str,
            required=True,
            help="A meal must contain a description"
        )
        args = parser.parse_args()
        ordered_date = dt.datetime.utcnow()
        status = "Pending"
        amount = args['price'] * args['qty']

        order_models.add_order(
            args['meal'],
            args['qty'],
            str(ordered_date),
            args['price'],
            status,
            args['description'],
            amount
        )

        return (
            {
                "status":"Success",
                "order":args
            }
        ), 201
class SingleOrders(Resource):
    """ This class will handle single orders made """
    @auth_required
    def get(self, identifier):
        result = order_models.get_order_by_id(identifier)
        if result:
            print(result)
            return (
                {
                    "status":"Success",
                    "order":{
                        "order_id":result[0],
                        "user_id":result[1],
                        "meal":result[2],
                        "ordered_date":result[3],
                        "delivered_date":result[4],
                        "price":result[5],
                        "qty":result[6],
                        "amount":result[7],
                        "status":result[8],
                        "description":result[9]
                    }
                }
            ), 200
        else:
            raise NotFound("Order of that identifier not found")
    @check_admin
    def put(self, identifier):
        result = order_models.get_order_by_id(identifier)
        if result:
            status = "Delivered"
            delivered_date = str(dt.datetime.now())
            order_models.update_status(identifier, status,delivered_date)
            return (
                {
                    "status":"Success, Order delivered"
                }
            ), 201
        else:
            raise NotFound("Order of that identifier was not found")

class UserOrders(Resource):
    """ This holds the endpoint for getting orders made by a specific user"""
    @check_admin
    def get(self, identifier):
        result = order_models.find_order_by_user_id(identifier)
        orders = []
        if result:
            for u in result:
                order = serialize.serialize_order(u)
                orders.append(order)
            return (
                {
                    "status":"Success",
                    "order":orders
                }
            ), 200
        else:
            raise NotFound("The user has not not placed any order")
