import os
import datetime as dt  

import jwt
from werkzeug.exceptions import BadRequest, NotFound

from app.database import init_database

class Commons(object):
    """ This class holds all methods that contain common actions used in the project """
    def __init__(self):
        self.db = init_database()

    @staticmethod
    def get_token(user_id):
        try: 
            payload = {
                "exp":dt.datetime.utcnow() + dt.timedelta(days=2),
                "iat":dt.datetime.utcnow,
                "sub":user_id
            }
            token = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
                algorithm="HS256"                
            )
            return token
        except Exception as e:
            raise BadRequest(e)

    def token_decoding(self, token):
        secret_key = os.getenv("SECRET_KEY")

        try:
            payload = jwt.decode(token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Am afraid the token has expired"
        except jwt.InvalidTokenError:
            return "Token is invalid"
        


        


