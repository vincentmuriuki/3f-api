import os

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound

from app.api.v2.models.db_vars import Database

email_query = "SELECT * FROM users WHERE email='%s'"
class UserModels(Database):
    """ This class will hold all methods for user authentication """    
    def __init__(self):  
        super().__init__()

    def email_exists(self, email):
        self.email = email
        self.cursor.execute(email_query % self.email)
        email_found = self.cursor.fetchone()
        if email_found:
            raise BadRequest("Email in use")
        else:
            return self.email       

    def create_user(self, data):        
        self.username = data['username']
        self.email = data['email']
        self.address = data['address']
        self.password = data['password']
        self.is_admin = data['is_admin']
        self.cursor.execute("""INSERT INTO users (username, email, password, address, is_admin) 
        VALUES (
            '%s', '%s', '%s', '%s', '%s'
        ) RETURNING user_id
        """ % (self.username, self.email, self.password, self.address, self.is_admin))
        user_id = self.cursor.fetchone()
        self.store()
        return user_id

    def get_login_email(self, email):
        self.cursor.execute(email_query % email)
        user_in = self.cursor.fetchone()
        return user_in

    def get_user_password(self, email):
        self.cursor.execute(email_query % email)
        hashed_password = self.cursor.fetchone()[3]
        return hashed_password

    def get_user_id(self, email):
        self.cursor.execute(email_query % email)
        user_id = self.cursor.fetchone()[0]
        return user_id

    def get_user_creds_with_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id='%s'" % user_id)
        user_details = self.cursor.fetchone()
        return user_details

    def token_blacklist(self, token):
        """
        This stores tokens used by users
        """
        self.cursor.execute("""INSERT INTO blacklist (user_tokens) VALUES ('%s')""" % token)
        self.store()
        return token

    def check_token_blacklist(self, token):
        """
        This checks for a blacklisted token
        """
        self.cursor.execute("SELECT * FROM blacklist WHERE user_tokens='%s'" % (token))
        token_blacklisted = self.cursor.fetchone()
        return token_blacklisted

        



        