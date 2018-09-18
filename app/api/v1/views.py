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
            }
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

        order =  [order for order in orders if order['id'] == identifier]
        if len(order) == 0:
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
        
        order = [order for order in orders if order['id'] == identifier]
        if len(order) == 0:
            return (
                {
                  "message":"Order of the identifier not found"
                }
            ), 404
        elif not request.json:
            return (
                {
                  "message":"Missing a field"
                }
            ), 400
        elif 'status' in request.json and type(request.json['status']) != bool:
            return (
                {
                    "message":"Missing a field"
                }
            ), 400
        else:
            order[0]['status'] = request.json.get('status', order[0]['status'])
            order

            return (
                {
                    'message':'Order delivered',
                    'order': order[0]
                }
            ), 201

    def delete(self, identifier):
        order = [order for order in orders if order['id'] == identifier]
        if len(order) == 0:
            return (
                {
                  "message":"Order of the id not found"
                }
            ), 404
        else:
            order.remove(order[0])
            return (
                {
                    "message":"Success, order deleted"
                }
            ), 204

class LandingPage(Resource):

    def get(self):
        return "Hi there, Welcome! visit my github develop branch read the readme file to test your apis. <a href='https://github/tesh254/3f-api.git'>Click here</a>"

api.add_resource(LandingPage, '/')
api.add_resource(Orders, '/api/v1/orders')
api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')

    
