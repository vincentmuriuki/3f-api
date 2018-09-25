import re
import string

from werkzeug.exceptions import BadRequest, NotFound

class Validators(object):
    def __init__(self):
        pass 

    def email_validator(self, email):
        self.email = email
        if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
            email):
            raise BadRequest("Please provide a valid email")
        else:
            return self.email

    def password_validator(self, password):
        self.password = password
        
        if len(self.password) < 6:
            raise BadRequest("Password is too short")
        elif len(self.password) > 12:
            raise BadRequest("Password too long")
        else:
            return self.password

    def username_validator(self, username):
        self.username = username

        for i in username:
            if i not in string.ascii_letters:
                raise BadRequest("Username should not contain digits")
            else:
                return self.username
                