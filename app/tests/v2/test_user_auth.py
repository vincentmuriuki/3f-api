import unittest
import json
import string


from app import create_app
from app.database import init_test_database, dismantle

class TestFlaskAuthentication(unittest.TestCase):
    """ This class contains all enpoint tests for authentication """

    def setUp(self):
            self.app = create_app("testing")
            self.client = self.app.test_client()

            self.user_creds = {
                "username":"Erick Wachira",
                "email":"ewachira254@gmail.com",
                "password":"asdfgh",
                "address":"Kawangware"
            }

            with self.app.app_context():
                self.db = init_test_database()

    def auth_data(self, path='/api/v2/auth/signup', data={}):
        """ This method holds neccesary data to facilitate the test for user signup """
        if not data:
            data = self.user_creds
        return (
            self.client.post(
                path, data=json.dumps(data), content_type='applications/json'
            )
        )

    def test_user_signup(self):
        """ This will test the user registration """
        response = self.auth_data(data=self.user_creds)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        """ This will test the user registration """
        data = {
            "email":self.user_creds['email'],
            "password":self.user_creds['password']
        }
        response = self.client.post(
            '/api/v2/auth/login', 
            data=json.dumps(data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        dismantle()


if __name__ == "__main__":
    unittest.main()
