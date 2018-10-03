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
        
        self.login_creds = {
            "email":"data@fmail.com",
            "password":"felisha"
        }

        self.response = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user_creds),
            content_type="application/json"
        )

    def create_user(self):
        self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(self.user_creds),
            content_type="application/json"
        )        

    def tearDown(self):
        with self.app.app_context():
                dismantle()
