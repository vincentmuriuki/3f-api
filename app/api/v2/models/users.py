import os

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized 

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

    def check_admin_in_db(self):
        """ This checks if an admin exists in the system """
        self.cursor.execute("SELECT * FROM users WHERE is_admin='%s'" % True)
        result = self.cursor.fetchall()
        self.store()
        if result:
            raise Unauthorized("Admin exists, request for user role upgrade")
        else:
            is_admin = True
            return is_admin

    def check_role_by_email(self, email):
        """ Check user role """
        self.cursor.execute(
            """
            SELECT * FROM users WHERE email='%s'
            """ % email
        )
        result = self.cursor.fetchone()
        if result:
            if result[5] == True:
                return result
            else:
                return None

    def update_user_role(self, email):
        """ This upgrades a user role in the site """
        self.cursor.execute(email_query % email)
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("""
                UPDATE users SET is_admin='%s' WHERE email='%s';
            """ % (True, email))
            return email
        else:
            return None
        



        