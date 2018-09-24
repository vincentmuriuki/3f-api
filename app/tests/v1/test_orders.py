import unittest
from app import create_app
import json

class TestFlaskApi(unittest.TestCase):
    """ This class contains all tests that test endpoints """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.order_data = {
            "username":"Erick Wachira",
            "product_name":"Hamburger",
            "price":450,
            "qty":5,
            "status":"Pending"
        }
        self.status = 'Delivered'
        self.order_id = 1   

    def post_data(self, path='/api/v1/orders', data_dict={}):
        data_dict = self.order_data
        result = self.client.post(path, data=json.dumps(data_dict), content_type = "application/json")

        return result


    def test_delete_all_orders(self):
        res = self.client.delete(
            '/api/v1/orders', 
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 204)

    def test_delete_specific_order(self):
        res = self.client.delete(
            '/api/v1/orders/{}'.format(self.order_id), 
            content_type='application/json'
        )

        if res.status_code == 404:
            # Test if an order is not found
            self.assertEqual(res.status_code, 404)
        else:
            # Test if the order was successfully deleted
            self.assertEqual(res.status_code, 204)   

    def test_get_specific_order(self):
        res = self.client.get(
            '/api/v1/orders/{}'.format(self.order_id), 
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 200) 

    def test_get_orders(self):
        res = self.client.get(
            '/api/v1/orders', 
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

    def test_updating_order_status(self):

        res = self.client.put(
            '/api/v1/orders/{}'.format(self.order_id), 
            data = json.dumps(self.status),
            content_type='application/json'
        )

        if res.status_code == 404:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 201)

    

    def test_place_an_order(self):
        res = self.post_data()

        self.assertEqual(res.status_code, 201)

if __name__ == "__main__":
    unittest.main()

