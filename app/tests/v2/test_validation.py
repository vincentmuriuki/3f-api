import unittest 
import os

from app.api.v2.validators.validators import Validators
from app.tests.v2.test_base_case import TestBaseCase

validate = Validators()

# class TestValidators(TestBaseCase):
#     """ Test the validator methods """
#     def test_valid_email_validation(self):
#         email = "hunnid@fmail.com"
#         validate_email = validate.email_validator(email)
#         self.assertEqual(validate_email, "hunnid@fmail.com")
