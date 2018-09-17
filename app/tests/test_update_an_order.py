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


if __name__ == "__main__":
    unittest.main()

