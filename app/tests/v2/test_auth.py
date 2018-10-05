import json 
import os

from app.tests.v2.test_base_case import TestBaseCase 
from app.api.v2.models.users import UserModels
from app.api.v2.helpers.token import TokenGen

user_models = UserModels()
token_gen = TokenGen()

class TestFlaskAuth(TestBaseCase):
    """ Test user auth """
    # def test_registration(self):
    #     response = self.client.post(
    #         "/api/v2/auth/signup",
    #         data=json.dumps(self.signup_data),
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, 201)

    def test_encode_token(self):
        user_id = user_models.create_user(self.sample_signup_data)
        token = token_gen.encode_auth_token(user_id)
        self.assertTrue(isinstance(token, bytes))


    def test_login(self):
        user_id = user_models.create_user(self.sample_signup_data)
        response = self.client.post(
            "/api/v2/auth/login",
            data=json.dumps(self.login_data),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['status'], "Success")
