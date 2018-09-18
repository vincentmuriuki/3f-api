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

api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')

    