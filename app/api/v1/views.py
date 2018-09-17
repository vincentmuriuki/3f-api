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
            return ({
                "message":"No orders yet"
            }),200

        return (
            {
                "orders":orders
            }            
        ), 200


