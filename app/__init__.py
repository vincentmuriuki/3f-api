from flask import Flask, Blueprint
from flask_restful import Api

# Local Import
from instance.config import app_config
from app.api.v1.views import Orders, OrdersManipulation, LandingPage
from app.api.v2.views.users import UserRegistration, UserLogin, UserLogout, User

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
    api.add_resource(UserLogout, '/api/v2/auth/logout')
    api.add_resource(User, '/api/v2/auth/profile')


    return app