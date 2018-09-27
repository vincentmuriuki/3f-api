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

            self.category_data = {
                "category_name":"Fried"
            }

            with self.app.app_context():
                self.db = init_test_database()

    def test_category_creation(self):
        """ This will test the category creation """
        response = self.client.post('/api/v2/categories', 
            data=json.dumps(self.category_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_getting_order(self):
        """ This will test the getting of all categories """
        response = self.client.get(
            '/api/v2/categories',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        dismantle()

if __name__ == "__main__":
    unittest.main()
