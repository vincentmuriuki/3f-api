from functools import wraps
import os

from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
import jwt

from app.api.v2.models.users import UserModels

user_models = UserModels()

def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify(
                {
                    "message":"Token is missing"
                }
            ), 401

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            current_user = user_models.get_user_creds_with_id(user_id=data['user_id'])
        except Exception as e:
            return jsonify(
                {
                    "message":"Token is invalid! this is why: {}".format(e)
                }
            ), 401

        return function(current_user, *args, **kwargs)

    return decorated
