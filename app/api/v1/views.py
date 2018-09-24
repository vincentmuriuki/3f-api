# import dependencies
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
import datetime as dt
import os
import markdown

#importing local modules
from .models import OrdersOperation

app = Flask(__name__)

api = Api(app)

orders_models = OrdersOperation()

orders = orders_models.get_orders()

class Orders(Resource):
    """ This class handles api endpoints that handle all orders in general. """
    def get(self):

        if len(orders) == 0:
            return (
                {
                    "message":"No orders yet"
                }
            ), 200
        return (
            {
                "orders":orders
            }
        ), 200

    def post(self):
        id = len(orders) + 1
        ordered_date = str(dt.datetime.now())
        delivered_date = None
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username',
            type=str,
            required=True,
            help="This field is required"
        )
        parser.add_argument(
            'product_name',
            type=str,
            required=True,
            help="This field is required"
        )
        parser.add_argument(
            'price',
            type=int,
            required=True,
            help="This field is required"
        )
        parser.add_argument(
            'qty',
            type=int,
            required=True,
            help="This field is required"
        )
        parser.add_argument(
            'status',
            type=str,
            required=True,
            help="This field is required"
        )

        args = parser.parse_args()

        new_order = orders_models.create_order(id, 
            args['username'], args['product_name'], 
            args['price'], args['status'], 
            args['qty'], ordered_date, delivered_date
        )

        return new_order, 201

    def delete(self):        
        orders = orders_models.get_orders()
        if len(orders) == 0:
            return (
                {
                    "message":"No orders to delete"
                }
            ), 204
        orders = []
        return (
            {
                "message":"Orders deleted"
            }
        ), 204

class OrdersManipulation(Resource):
    """ This class holds all api enpoints that handle specific order enpoints """
    def get(self, identifier):
        order = orders_models.get_specific_order(identifier)

        if order is None:
            return (
                {
                    "message":"Order not found"
                }
            ), 404
        return (
            {
                "message": "Success",
                "order":order

            }
        ), 200

    def put(self, identifier):
        order = orders_models.get_specific_order(identifier)

        if order:
            order[0]['status'] = "Delivered"
            order[0]['delivered_date'] = str(dt.datetime.now())
            return (
                {
                    "message":"Order has been delivered"
                }
            ), 201
        return(
            {
                "message":"Order not found"
            }
        ), 404

    def delete(self, identifier):
        order = orders_models.get_specific_order(identifier)
        if not order:
            return (
                {
                  "message":"Order of the id not found"
                }
            ), 404
        orders.remove(order[0])
        return (
            {
                "message":"Success, order deleted"
            }
        ), 204

class LandingPage(Resource):
    """ This class handles the endpoint for the landing page """
    def get(self):        
        return """Copy this link to visit my git repo for the docs: https://github.com/tesh254/3f-api """




    
