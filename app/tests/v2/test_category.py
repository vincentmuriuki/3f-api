import unittest
import json
import string

import psycopg2
from flask import request

from app.api.v2.helpers.token import TokenGen
from app.tests.v2.test_base_case import BaseTestCase

token_gen = TokenGen()

class TestCategories(BaseTestCase):
    """ Test the endpoints handling categories """
    def test_get_categories(self):
        token = self.create_user()
        response = self.client.get(
            "/api/v2/admin/categories",
            data = json.dumps(self.category_data),
            headers = {"Authorization":token},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        
    def test_create_category(self):
        response = self.client.post(
            "/api/v2/admin/categories",
            data = json.dumps(self.category_data),
            headers={"Authorization":self.create_user()},
            content_type="application/json"
        )

        self.assertTrue(response.status_code==201)


if __name__ == "__main__":
    unittest.main()