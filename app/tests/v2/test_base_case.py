import unittest
import json
import string

import psycopg2
from flask import request

from app import create_app
from app.database import init_test_database, dismantle
from app.api.v2.models.users import UserModels
from app.api.v2.helpers.token import TokenGen

user_models = UserModels()
token_gen = TokenGen()

class BaseTestCase(unittest.TestCase):
    """ This is the base test case holding the setup method """
    def setUp(self):            
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            init_test_database()

        self.category_data = {
            "category_name":"Fried"
        }

        self.user_creds = {
            "username":"Erick Wachira",
            "email":"data@fmail.com",
            "password":"felisha",
            "address":"Thika",
            "user_type":True
        }

        self.order_creds = {
            {
                "meal":"Magarita Pizza",
                "qty":2,
                "price":1200,
                "description":"Less fats used"
            }
        }
        
        self.login_creds = {
            "email":"data@fmail.com",
            "password":"felisha"
        }

        self.order_id = 1
        self.user_id = 1

        self.response = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user_creds),
            content_type="application/json"
        )

    def create_user(self):
        """ Create user to get token for authorization """
        user_id = user_models.create_user(self.user_creds)
        token = token_gen.encode_auth_token(user_id)
        token = token.decode()
        return token

    def tearDown(self):
        with self.app.app_context():
                dismantle()
