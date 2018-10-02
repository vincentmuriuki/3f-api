import os
import json
import datetime as dt

from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, Resource, Api
from werkzeug.exceptions import Conflict, Unauthorized, BadRequest, NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.users import UserModels
from app.api.v2.validators.validators import Validators
from app.api.v2.helpers.token import TokenGen

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
            'user_type',
            type=bool,
            required=False,
            default=False
        )
        args = parser.parse_args()
        email = validate.email_validator(args['email'])
        password = validate.password_validator(args['password'])
        username = validate.username_validator(args['username'])
        hashed_password = generate_password_hash(password, method='sha256')
        new_email = user_models.email_exists(email)
        try:
            new_user = {
                "email":new_email,
                "username":username,
                "password":hashed_password,
                "address":args['address'],
                "user_type":args['user_type']
            }
            user_id = user_models.create_user(new_user)
            print(user_id)
            auth_token = token_gen.encode_auth_token(user_id)        
            return(
                {
                    "status":"Success",
                    "message":"User created successfully",
                    "auth_token":str(auth_token.decode()),
                    "user_id":user_id
                }
            ), 201
        except Exception as e:
            print(e)

    
class UserLogin(Resource):
    """ This class holds the endpoint for user login """
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email', 
            type=str,
            required=True,
            help="An email is required to login",
        )
        parser.add_argument(
            'password', 
            type=str,
            required=True,
            help="A password is required"
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
                            "auth_token":str(auth_token.decode())
                        }
                    ), 200
                else:
                    raise BadRequest("Token not created")
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
                user = user_models.get_user_creds_with_id(user_id=response)
                if not user[5]:
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
                            "message":"No user of that id"
                        }
                    ), 404
            else:
                return (
                    {
                        "message":"Something went wrong"
                    }
                ), 401
        else:
            return (
                    {
                        "message":"Something went wrong"
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
                    "message":"Something went wrong"
                }
            ), 401
        return (
            {
                "message":"Token not data"
            }
        ), 400



