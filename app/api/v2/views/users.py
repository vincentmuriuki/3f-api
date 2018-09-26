import os

from flask import Flask, request
from flask_restful import reqparse, Resource, Api
import jwt
from werkzeug.exceptions import Conflict, Unauthorized, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.users import UserModels
from app.api.v2.validators.validators import Validators
from app.api.v2.validators.commons import Commons

user_models = UserModels()
validate = Validators()
common = Commons()

class UserRegistration(Resource):
    """ This class holds the endpoint for user registration """
    
    def get(self):
        return "This is the signup page"

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
        
        args = parser.parse_args()

        email = validate.email_validator(args['email'])
        username = validate.username_validator(args['username'])
        password = validate.password_validator(args['password'])

        print(args['address'])

        user_id = user_models.user_signup(
            username,
            email, 
            password,
            str(args['address'])
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

class UserLogin(Resource):
    def get(self):
        return "This is the login page"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',
            type=str,
            required=True,
            help="An email is required to login"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="A password is needed for you to login"
        )
        args = parser.parse_args()
        user = user_models.get_login_email(args['email'])
        if not user:
            raise Unauthorized("The email does not exist, please register")
        user_id, email, username, password, user_type = user
        if not check_password_hash(password, args["password"]):
            raise Unauthorized("The email or password is incorrect")
        token = common.get_token(int(user_id))
        return (
            {
                "message":"Successful Login",
                "AuthToken":token.decode('utf-8')
            }
        ), 200

class UserLogout(Resource):
    """ This endpoint serves the logout of a user """
    def get(self):
        return "You about to logout"
    def post(self):
        header = request.headers.get("Authorization")
        if not header:
            raise BadRequest(
                "No access"
            )
        auth_token = header.split(" ")[1]
        response = common.token_decoding(auth_token)
        if isinstance(response, str):
            raise Unauthorized(
                "You are not allowed"
            )
        else:
            user_token = user_models.user_logout(auth_token)
            return (
                {
                    "message":"Logout done, hope you come soon"
                }
            ), 200
        


