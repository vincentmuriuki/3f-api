# import dependencies
from flask import Flask, request, abort
from flask_restful import Resource, Api
import datetime

#importing local modules
from .models import OrdersOperation

app = Flask(__name__)

api = Api(app)

db = OrdersOperation()

orders = db.get_orders()

class Orders(Resource):
    def get(self):

        if len(orders) == 0:
            return (
                {
                    "message":"No orders yet"
                }
            ), 200
        else:
            return (
                {
                    "orders":orders
                }
            ), 200

    def post(self):

        data_json = request.get_json()

        new_order = {
            "id":len(orders) + 1,
            "username":data_json['username'],
            "products":{
                "name":data_json['products']['name'],
                "qty":data_json['products']['qty'],
                "price":data_json['products']['price']
            },
            "status":"Pending",
            "ordered_date":str(datetime.datetime.now()),
            "delivered_date":None
        }

        orders.append(new_order)

        return (
            {
                "message":"Success",
                "order":new_order
            }
        ), 201

class OrdersManipulation(Resource):
    def get(self, identifier):

        order = db.get_specific_order(identifier)

        if order is None:
            return (
                {
                    "message":"Order not found"
                }
            ), 404
        else:
            return (
                {
                    "message": "Success"
                }
            ), 200
    def put(self, identifier):
        order = db.get_specific_order(identifier)

        if order:
            order[0]['status'] = "Delivered"
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
        order = db.get_specific_order(identifier)
        if order is None:
            return (
                {
                  "message":"Order of the id not found"
                }
            ), 404
        else:
            orders.remove(order)
            return (
                {
                    "message":"Success, order deleted"
                }
            ), 204

class LandingPage(Resource):

    def get(self):
        return ""



    
