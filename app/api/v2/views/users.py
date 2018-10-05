import os
import json
import datetime as dt
import base64

from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, Resource, Api
from werkzeug.exceptions import Conflict, Unauthorized, BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.users import UserModels
from app.api.v2.validators.validators import Validators
from app.api.v2.helpers.token import TokenGen
from app.api.v2.helpers.helpers import check_admin

user_models = UserModels()
validate = Validators()
token_gen = TokenGen()

class UserRegistration(Resource):
    """ This class holds the endpoint for user registration """
    
    def get(self):
        return "This is the signup page"

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email',
            type=str,
            required=True,
            help='An email is required to signup'
        )
        parser.add_argument(
            'username', 
            type=str,
            required=True,
            help="A username is required to login"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="You need a password to secure your account"
        )
        parser.add_argument(
            'address',
            type=str,
            required=True,
            help="We need an address"
        )
        parser.add_argument(
            'is_admin',
            type=bool,
            required=True,
            help="You need to specify your role"
        )
        args = parser.parse_args()
        email = validate.email_validator(args['email'])
        password = validate.password_validator(args['password'])
        username = validate.username_validator(args['username'])
        hashed_password = generate_password_hash(password, method='sha256')
        new_email = user_models.email_exists(email)
        if args['is_admin'] == True:
            is_admin = user_models.check_admin_in_db()
            try:
                new_user = {
                    "email":new_email,
                    "username":username,
                    "password":hashed_password,
                    "address":args['address'],
                    "is_admin":is_admin
                }
                user_id = user_models.create_user(new_user)  
                return(
                    {
                        "status":"Success",
                        "message":"User created successfully"
                    }
                ), 201
            except Exception as e:
                raise BadRequest("Something is wrong maybe it is this {} ".format(e))
        try:
            new_user = {
                "email":new_email,
                "username":username,
                "password":hashed_password,
                "address":args['address'],
                "is_admin":args['is_admin']
            }
            user_id = user_models.create_user(new_user)  
            return(
                {
                    "status":"Success",
                    "message":"User created successfully"
                }
            ), 201
        except Exception as e:
            raise BadRequest("Something is wrong maybe it is this {} ".format(e))

    
class UserLogin(Resource):
    """ This class holds the endpoint for user login """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email',
            type=str,
            required=True,
            help="Well you cannot log in with no email provided"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Well you need a password, dont you!!!"
        )
        args = parser.parse_args()
        status = user_models.get_login_email(args['email'])
        if status:
            if check_password_hash(status[3], args['password']):
                auth_token = token_gen.encode_auth_token(status[0])            
                if auth_token:
                    return (
                        {
                            "status":"Success",
                            "message":"Successfully logged in.",
                            "auth_token":auth_token.decode("utf-8")
                        }
                    ), 200
                else:
                    raise NotFound("Token not created")
            else:
                raise BadRequest("Passwords do not match")
        else:
            raise NotFound("The email you provided does not exists")

class User(Resource):
    """
    Get user credentials
    """
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            response = token_gen.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user = user_models.get_user_creds_with_id(response)
                if user:
                    return (
                        {
                            "status":"Success",
                            "user_credentials":{
                                "user_id":response,
                                "email":user[2],
                                "user_type": user[5]
                            }
                        }
                    ), 200
                
                return (
                        {
                            "status":"Fail",
                            "message":"No user of that id {}".format(response)
                        }
                    ), 404
            else:
                return (
                    {
                        "message":"You have a session problem please login"
                    }
                ), 401
        else:
            return (
                    {
                        "message":"Please login to start a session"
                    }
                ), 401

class UserLogout(Resource):
    """
    Api endpoint to facilitate the logging out of a user
    """
    def post(self):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token=''
        if auth_token:
            response = token_gen.decode_auth_token(auth_token)
            if not isinstance(response, str):
                blacklist_token = user_models.token_blacklist(auth_token)
                return (
                    {
                        "status":"Success",
                        "message":"You logged out",
                        "token_status":"Your token: {} is blacklisted".format(blacklist_token)
                    }
                ), 200
            return (
                {
                    "message":"You logged out, please login to start a new session"
                }
            ), 401
        return (
            {
                "message":"Token not data"
            }
        ), 400

class UserUpgrade(Resource):
    """ Update a user to an admin api endpoints """
    @check_admin
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Enter the email for user role upgrade"
        )
        args = parser.parse_args()
        email = validate.email_validator(args['email'])
        if email:
            result = user_models.update_user_role(email)
            if result:
                return (
                    {
                        "status":"Success",
                        "message":"User of email {} status has been updated".format(email)
                    }
                ), 201
            else:
                return (
                    {
                        "status":"The email does not exist, check spelling"
                    }
                ), 401




