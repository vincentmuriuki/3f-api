from flask import Flask, Blueprint
from flask_restful import Api

# Local Import
from instance.config import app_config
from app.api.v1.views import Orders, OrdersManipulation, LandingPage
from app.api.v2.views.users import UserRegistration, UserLogin, UserLogout

def create_app(configuration):

    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    #app.config.from_pyfile('config.py')
    api = Api(app)
    api.add_resource(LandingPage, '/')
    api.add_resource(Orders, '/api/v1/orders')
    api.add_resource(OrdersManipulation, '/api/v1/orders/<int:identifier>')
    api.add_resource(UserRegistration, '/api/v2/auth/signup')    
    api.add_resource(UserLogin, '/api/v2/auth/login')


    return app