from flask import Flask, request, abort
from flask_restful import Resource, Api
import datetime

app = Flask(__name__)

api = Api(app)

orders = []
class Orders(Resource):
    def get(self):
        
        if len(orders) == 0:
            return ({
                "message":"No orders yet"
            }),201
        return (
            {
                "orders":orders
            }            
        ), 201

    def post(self):

        request_data = request.get_json()
        
        # new order dictionary to be added to the rest of the orders
        new_order = {
            'id':len(orders) + 1,
            'user_name':request_data['user_name'],
            'products':{
                "name":request_data['products']['name'],
                "qty":request_data['products']['qty'],
                "price":request_data['products']['price']
            },
            'status':False,
            'ordered_date': str(datetime.datetime.now()),
            'delivered_date':None
        }

        orders.append(new_order)

        return (
            {
                "message":"Created",
                "order":new_order
            }
        )