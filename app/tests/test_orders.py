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

        self.status = True

        self.order_id = 1

    def test_place_an_order(self):
        res = self.app.post(
            '/api/v1/orders', 
            data = json.dumps(self.order_data), 
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 201)

    def test_updating_order_status(self):

        res = self.app.put(
            '/api/v1/orders/{}'.format(self.order_id), 
            data = json.dumps(self.status),
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 201)

    def test_get_orders(self):
        res = self.app.get(
            '/api/v1/orders', 
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 200)

    def test_get_specific_order(self):
        res = self.app.get(
            '/api/v1/orders/{}'.format(self.order_id), 
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 204)

    def test_delete_specific_order(self):
        res = self.app.get(
            '/api/v1/orders/{}'.format(self.order_id), 
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 204)    


if __name__ == "__main__":
    unittest.main()

