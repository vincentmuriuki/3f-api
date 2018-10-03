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

class TestFlaskAuthentication(unittest.TestCase):
    """ This class contains all enpoint tests for authentication """

    def setUp(self):
            self.app = create_app("testing")
            self.client = self.app.test_client()

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

            with self.app.app_context():
                self.db = init_test_database()

    def test_decoding_token(self):
        user_id = user_models.create_user(self.user_creds)
        auth_token = token_gen.encode_auth_token(user_id)        
        self.assertTrue(isinstance(auth_token, bytes))

    def test_user_signup(self):
        with self.client:
            register_response = self.client.post(
                '/api/v2/auth/signup',
                data=json.dumps(self.user_creds),
                content_type='application/json'
            )
            data = json.loads(register_response.data.decode())
            self.assertEqual(register_response.status_code, 201)
            self.assertTrue(data['status'] == 'Success')
            self.assertTrue(data['message'] == 'User created successfully')
            self.assertTrue(data['auth_token'])
            self.assertTrue(register_response.content_type == 'application/json')

    def tearDown(self):
        with self.app.app_context():
                dismantle()


if __name__ == "__main__":
    unittest.main()
