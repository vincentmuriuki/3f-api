import os

from flask import Flask
from flask_restful import reqparse, Resource, Api
import jwt
from werkzeug.exceptions import Conflict

from app.api.v2.models.users import UserModels
from app.api.v2.validators.validators import Validators
from app.api.v2.validators.commons import Commons

user_models = UserModels()
validate = Validators()
common = Commons()

class UsersRestration(Resource):
    
    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email',
            type=str,
            required=True,
            help="An email should be provided"
        )
        parser.add_argument('username',
            type=str,
            required=True,
            help="A username is a required field"
        )
        parser.add_argument('address',
            type=str,
            required=True,
            help="An addresss is a required field"
        )
        parser.add_argument("password", 
            type=str,
            required=True,
            help="A password is a required field"
        )
        parser.add_argument('user_type',
            type=bool,
            required=False
        )
        
        args = parser.parse_args()

        email = validate.email_validator(args['email'])
        username = validate.username_validator(args['username'])
        password = validate.password_validator(args['password'])

        user_id = user_models.user_signup(
            username,
            email, 
            password,
            args['address'],
            args['user_type']
        )

        if not user_id:
            raise Conflict("Something went wrong when creating an account")
        else:
            token = common.get_token(user_id)
            return (
                {
                    "message":"Account Created",
                    "AuthToken":"{}".format(token.decode('utf-8'))
                }
            ), 201




