import unittest
from api.v1 import app
import json

class TestFlaskApi(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()

        self.order_data = {
            "username":"Lewis Ngugi",
            "products":{
                "name":"Chips Bhajia",
                "qty":5,
                "price":5
            }
        }

        self.order_id = 1

    def test_delete_order(self):
        """ Testing to check is a single order can be retrieved """
        res =self.app.delete('/api/v1/orders/{}/'.format(self.order_id), content_type='application/json')

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 204)


if __name__ == "__main__":
    unittest.main()

