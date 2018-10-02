import os

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound

from app.database import init_database, init_test_database

email_query = "SELECT * FROM users WHERE email='%s'"
class UserModels(object):
    """ This class will hold all methods for user authentication """    
    def __init__(self):  
        if os.getenv("CONFIG_TYPE") == "testing":
            self.db = init_test_database()
        else:
            self.db = init_database()

    def email_exists(self, email):
        self.email = email
        curr = self.db.cursor()
        curr.execute(email_query % self.email)
        email_found = curr.fetchone()
        if email_found:
            raise BadRequest("Email in use")
        else:
            return self.email       

    def create_user(self, data):        
        self.username = data['username']
        self.email = data['email']
        self.address = data['address']
        self.password = data['password']
        self.user_type = data['user_type']

        curr = self.db.cursor()
        curr.execute("""INSERT INTO users (username, email, password, address, user_type) 
        VALUES (
            '%s', '%s', '%s', '%s', '%s'
        ) RETURNING user_id
        """ % (self.username, self.email, self.password, self.address, self.user_type))
        user_id = curr.fetchone()
        self.db.commit()
        return user_id

    def get_login_email(self, email):
        curr = self.db.cursor()
        curr.execute(email_query % email)
        user_in = curr.fetchone()
        return user_in

    def get_user_password(self, email):
        curr = self.db.cursor()
        curr.execute(email_query % email)
        hashed_password = curr.fetchone()[3]
        return hashed_password

    def get_user_id(self, email):
        curr = self.db.cursor()
        curr.execute(email_query % email)
        user_id = curr.fetchone()[0]
        return user_id

    def get_user_creds_with_id(self, user_id):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM users WHERE user_id='%s'" % user_id)
        user_details = curr.fetchone()
        return user_details

    def token_blacklist(self, token):
        """
        This stores tokens used by users
        """
        curr = self.db.cursor()
        curr.execute("""INSERT INTO blacklist (user_tokens) VALUES ('%s')""" % token)
        self.db.commit()
        return token
    def check_token_blacklist(self, token):
        """
        This checks for a blacklisted token
        """
        curr = self.db.cursor()
        curr.execute("SELECT * FROM blacklist WHERE user_tokens='%s'" % (token))
        token_blacklisted = curr.fetchone()
        return token_blacklisted

        



        