# import dependencies
from flask import Flask, request, abort
from flask_restful import Resource, Api
import datetime

#importing local modules
from .models import Database

app = Flask(__name__)

api = Api(app)

db = Database()

orders = db.get_orders()

class Orders(Resource):
    def post(self):
        request_data = request.get_json()

        new_order = {
            'id': len(orders) + 1,
            'username':request_data['username'],
            'products':{
                "name":request_data['products']['name'],
                "qty":request_data['products']['qty'],
                "price":request_data['products']['price']
            },
            'status':False,
            'ordered_date':str(datetime.datetime.now()),
            'delivered_date':None
        }

        if not request_data['username'] or not request_data['products'] or not request_data:
            return (
                {
                    "message":"Oops missing field, Try again"
                }
            ), 400

        orders.append(new_order)

        return (
            {
                "message":"Successfull order",
                "order":new_order
            }
        ), 201

    api.add_resource(Orders, '/api/v1/orders')

    