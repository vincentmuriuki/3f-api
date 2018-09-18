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
class OrderManipulation(Resource):
    def get(self, identifier):

        order = [order for order in orders if order['id'] == identifier]

        if len(order) == 0:
            return (
                {
                    "message":"Order of that id not found"
                }
            ), 404
        
        return (
            {
                "message":"Success",
                "order":order
            }
        )

        