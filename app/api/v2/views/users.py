import os
import json
import datetime as dt

from flask import Flask, request, jsonify, make_response
from flask_restful import reqparse, Resource, Api
import jwt
from werkzeug.exceptions import Conflict, Unauthorized, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from app.api.v2.models.users import UserModels
from app.api.v2.validators.validators import Validators

user_models = UserModels()
validate = Validators()

class UserRegistration(Resource):
    """ This class holds the endpoint for user registration """
    
    def get(self):
        return "This is the signup page"

    def post(self):
        data = request.get_json()
        email = validate.email_validator(data['email'])
        password = validate.password_validator(data['password'])
        username = validate.username_validator(data['username'])
        hashed_password = generate_password_hash(password, method='sha256')
        new_email = user_models.email_exists(email)
        user_id = user_models.create_user(username=username, email=new_email, address=data['address'], password=hashed_password, user_type=False)
        return(
            {
                "message":"User created successfully",
                "user_id":user_id[0]
            }
        ), 201

    
class UserLogin(Resource):
    """ This class holds the endpoint for user login """
    def post(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response(
                'Could not verify',
                401,
                {
                    'WWW-Authenticate':'Basic realm="Login required"'
                }
            )
        
        user = user_models.get_login_email(auth.username)
        if not user:
            return make_response(
                'Could not verify',
                401,
                {
                    'WWW-Authenticate':'Basic realm="Login required"'
                }
            )

        hashed_password = user_models.get_user_password(auth.username)
        user_id = user_models.get_user_id(auth.username)
        if check_password_hash(hashed_password, auth.password):
            token = jwt.encode(
                {
                    "user_id":user_id,
                    "exp":dt.datetime.utcnow() + dt.timedelta(minutes=180),
                },
                os.getenv("SECRET_KEY"),
                algorithm="HS256"
            )
            return (
                {
                    'token':token.decode('UTF-8')
                }
            )

        return make_response(
                'Could not verify',
                401,
                {
                    'WWW-Authenticate':'Basic realm="Login required"'
                }
        )    

class UserLogout(Resource):
    """ This endpoint serves the logout of a user """
    pass



