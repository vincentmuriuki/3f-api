from functools import wraps
import os

from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed
import jwt

from app.api.v2.models.users import UserModels
from app.api.v2.helpers.token import TokenGen

token_gen = TokenGen()

user_models = UserModels()

def check_admin(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
            raise BadRequest("You need to login with admin credentials")
        
        if auth_token:
            response = token_gen.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user_credentials = user_models.get_user_creds_with_id(user_id=response[0])
                if not user_credentials[5]:
                    raise BadRequest("You dont have admin credentials")
                
                return function(*args, **kwargs)
    return decorated

def auth_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''

        if auth_token:
            response = token_gen.decode_auth_token(auth_token)
            if not isinstance(response, str):
                user_credentials = user_models.get_user_creds_with_id(user_id=response)
                if not user_credentials[5]:
                    raise BadRequest("You need to signup or login")
                
                return function(*args, **kwargs)

    return decorated
