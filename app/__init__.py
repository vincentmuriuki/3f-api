from flask import Flask, Blueprint
from flask_restful import Api

# Local Import
from instance.config import app_config
from app.api.v1.views import Orders, OrdersManipulation, LandingPage

def create_app(configuration):

    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    #app.config.from_pyfile('config.py')
    api = Api(app)
    api.add_resource(LandingPage, '/')
    api.add_resource(Orders, '/api/v1/orders')
    api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')

    return app