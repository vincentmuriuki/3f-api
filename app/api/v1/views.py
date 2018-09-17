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
        pass

api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')

    