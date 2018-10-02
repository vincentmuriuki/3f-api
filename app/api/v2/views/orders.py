import datetime as dt 
import json

from werkzeug.exceptions import BadRequest, NotFound
from flask_restful import Resource, reqparse

from app.api.v2.models.orders import OrderModels
from app.api.v2.helpers.helpers import auth_required, check_admin

order_models = OrderModels()

class OrdersMain(Resource):
    """ This class holds the endpoints for orders as a whole """
    @auth_required
    def get(self):
        orders = order_models.get_orders()
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

    def put(self, identifier):
        result = order_models.get_order_by_id(identifier)
        if result:
            status = "Delivered"
            delivered_date = dt.datetime.now()
            order_models.update_status(identifier, status, delivered_date)
            delivered_date = str(dt.datetime.now())
            order_models.update_status(identifier, delivered_date)
            return (
                {
                    "status":"Success, Order delivered"
                }
            ), 201
        else:
            raise NotFound("Order of that identifier was not found")

