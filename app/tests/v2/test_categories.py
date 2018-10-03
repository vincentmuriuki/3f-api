import unittest
import json
import string


from app import create_app
from app.database import init_test_database, dismantle

class TestFlaskCategory(unittest.TestCase):
    """ This class contains all enpoint tests for authentication """

    def setUp(self):
            self.app = create_app("testing")
            self.client = self.app.test_client()
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
            with self.app.app_context():
                self.db = init_test_database()

    def test_category_creation(self):
        """ This will test the category creation """
        response = self.client.post('/api/v2/admin/categories', 
            data=json.dumps(self.category_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_getting_categories(self):
        """ This will test the getting of all categories """
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
            response = self.client.get(
                '/api/v2/admin/categories',
                header=dict(
                Authorization=json.loads(
                    register_response.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
                dismantle()

if __name__ == "__main__":
    unittest.main()
