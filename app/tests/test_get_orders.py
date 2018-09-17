import unittest
from views import app

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

    def test_get_orders(self):
        response = self.app.get(
            '/api/v1/orders',
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

