from flask import Flask 
from flask_restful import Api
from instance import config
from app.api.v1.views import Orders, OrdersManipulation, LandingPage

def create_app(configuration):

    app = Flask(__name__)
    app.config.from_object(config.app_config[configuration])

    api = Api(app)

    api.add_resource(LandingPage, '/')
    api.add_resource(Orders, '/api/v1/orders')
    api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')


    return app