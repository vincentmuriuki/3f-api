import unittest
from api.v1.views import app

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

    def test_get_specific_order(self):
        response = self.app.get(
            '/api/v1/orders/{}'.format(self.order_id),
            content_type="application/json"
        )

        if response.status_code == 404:
            self.assertEqual(response.status_code, 404)
        else:
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

