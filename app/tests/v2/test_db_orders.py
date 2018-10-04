import unittest
import json
import string

import psycopg2
from flask import request

from app.api.v2.helpers.token import TokenGen
from app.tests.v2.test_base_case import BaseTestCase

token_gen = TokenGen()

class TestOrders(BaseTestCase):
    """ Test the endpoints handling categories """
    def test_get_orders_made_by_users(self):
        token = self.create_user()
        response = self.client.get(
            "/api/v2/admin/orders",
            data = json.dumps(self.category_data),
            headers = {"Authorization":token},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)  

    def test_placing_of_an_order(self):
        token = self.create_user()
        response = self.client.post(
            "/api/v2/user/orders",
            data=json.dumps(self.order_creds),
            headers={"Authorization":token},
            content_type="application/json"
        )      
        self.assertEqual(response.status_code, 201)

    def test_get_user_specific_order(self):
        response = self.client.get(
            "/api/v2/user/orders/{}".format(self.user_id),
            headers={"Authorization":self.create_user()},
            content_type="application/json"
        )
        
        self.assertTrue(response.status_code==200)

    def test_get_orders_made_by_user(self):
        token = self.create_user()
        response = self.client.get(
            "/api/v2/user/orders",
            headers={"Authorization":token},
            content_type="application/json"
        )

        self.assertTrue(response.status_code==200)

    def test_get_specific_order(self):
        response = self.client.get(
            "/api/v2/orders/{}".format(self.order_id),
            headers={"Authorizaiton":self.create_user()},
            content_type="application/json"
        )

        self.assertTrue(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()