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
            "address":"Emba",
            "password":"felisha",
            "is_admin":True
        }
        self.sample_signup_data = {
            "username":"Mirani",
            "email":"data@fmail.com",
            "address":"Emba",
            "password":generate_password_hash("felisha"),
            "is_admin":True
        }
        self.login_data = {
            "email":"data@fmail.com",
            "password":"felisha"
        }
