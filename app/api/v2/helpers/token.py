import datetime as dt
import os

import jwt 

from app.api.v2.models.users import UserModels

user_models = UserModels()

class TokenGen(object):

    def __init__(self):
        pass

    def encode_auth_token(self, user_id):
        """ Generate the Auth Token 
            :return: String
        """
        try:
            payload = {
                'exp': dt.datetime.utcnow() + dt.timedelta(days=0, minutes=180),
                'iat':dt.datetime.utcnow(),
                'sub':user_id
            }
            return jwt.encode(
                payload, 
                os.getenv("SECRET_KEY" or "5PAVHUG4HuYaCjDvMTPBmnHV3bRamRxx"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth_token
        :param auth_token:
        :return: integer|string
        """

        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY' or "5PAVHUG4HuYaCjDvMTPBmnHV3bRamRxx"))
            is_blacklisted_token = user_models.check_token_blacklist(auth_token)
            if is_blacklisted_token:
                return "Token cannot be used. Log in to get one"                
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired'
        except jwt.InvalidTokenError:
            return 'Token Invalid'
