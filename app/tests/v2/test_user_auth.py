import unittest
import json
import string

import psycopg2
from flask import request

from app.database import init_test_database, dismantle
from app.api.v2.models.users import UserModels
from app.api.v2.helpers.token import TokenGen
from app.tests.v2.test_base_case import BaseTestCase

user_models = UserModels()
token_gen = TokenGen()

class TestFlaskAuthentication(BaseTestCase):
    """ This class contains all enpoint tests for authentication """
    def test_decoding_token(self):
        user_id = user_models.create_user(self.user_creds)
        auth_token = token_gen.encode_auth_token(user_id)        
        self.assertTrue(isinstance(auth_token, bytes))

    def test_user_signup(self):
        """ Test the registration of a user """
        self.assertEqual(self.response.status_code, 201)
        self.assertTrue(self.response.json['auth_token'])
        self.assertTrue(self.response.content_type == "application/json")

if __name__ == "__main__":
    unittest.main()
