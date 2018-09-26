import os
import json

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
        data = request.data.decode().replace("'", '"')
        if not data:
            raise BadRequest("Enter all fields")
        user_creds = json.loads(data)

        email = validate.email_validator(user_creds['email'])
        username = validate.username_validator(user_creds['username'].split())
        password = validate.password_validator(user_creds['password'].split())

        new_user = {
            'email':email,
            'username':username,
            'password':password,
            'address':user_creds['address'].split()
        }

        user_id = user_models.user_signup(new_user)     

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
        


