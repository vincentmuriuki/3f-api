import unittest
import json
import string

import psycopg2

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
                "email":"ewachira254@gmail.com",
                "password":"asdfgh",
                "address":"CBD",
                "user_type":True
            }

            with self.app.app_context():
                self.db = init_test_database()

    def test_decoding_token(self):
        user_id = user_models.create_user(self.user_creds)
        try:
            auth_token = token_gen.encode_auth_token(user_id)
        except psycopg2.ProgrammingError as e:
            print(e)

        
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(token_gen.decode_auth_token(auth_token) == 1)

    def test_user_signup(self):
        response = self.client.post(
            '/api/v2/auth/signup',
            data=json.dumps(dict(
                username="Erick Wachira",
                email="data@fmail.com",
                password="felisha",
                address="Thika",
                user_type=True
            )),
            content_type='application/json'
        )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)
   

    def tearDown(self):
        dismantle()


if __name__ == "__main__":
    unittest.main()
