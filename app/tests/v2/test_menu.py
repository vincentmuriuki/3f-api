import unittest
import json
import string

import psycopg2
from flask import request

from app.api.v2.helpers.token import TokenGen
from app.tests.v2.test_base_case import BaseTestCase

token_gen = TokenGen()

class TestMenu(BaseTestCase):
    """ This class holds the testing of menu related """
    def test_get_menu(self):
        """ Test getting of the menu """
        response = self.client.get(
            "/api/v2/menu",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        
        


if __name__ == "__main__":
    unittest.main()