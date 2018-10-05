import unittest
import os
import json

from werkzeug.security import generate_password_hash

from app import create_app
from app.api.v2.models.users import UserModels
from testdb import Table_Manipulation

user_models = UserModels()

class TestBaseCase(unittest.TestCase):
    """ 
    This class holds the setup method and any data needed in the test 
    """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db = Table_Manipulation()
            db.drop()
            db.create_tables_to_be_used()
          

        self.signup_data = {
            "username":"Mirani",
            "email":"data@fmail.com",
            "username":"Amaza",
            "address":"Emba",
            "password":"felisha",
            "is_admin":True
        }
        self.sample_signup_data = {
            "username":"Mirani",
            "email":"data@fmail.com",
            "username":"Amaza",
            "address":"Emba",
            "password":generate_password_hash("felisha"),
            "is_admin":True
        }
        self.login_data = {
            "email":"data@fmail.com",
            "password":"felisha"
        }

    def test_registration(self):
        response = self.client.post(
            "/api/v2/auth/signup",
            data=json.dumps(self.signup_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        user_id = user_models.create_user(self.sample_signup_data)
        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(self.login_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)