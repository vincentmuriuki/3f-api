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

class OrdersManipulation(Resource):
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

            return (
                {
                    'message':'Order delivered',
                    'order': order[0]
                }
            ), 201

api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')

    