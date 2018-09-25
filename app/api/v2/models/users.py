import os

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound

from app.database import init_database

class UserModels(object):
    """ This class will hold all methods for user authentication """    
    def __init__(self):
        self.conn = init_database()
        query  = """
            SELECT * FROM users 
        """
        self.cursor = self.conn.cursor()
        self.cursor.excute(query)
        self.users = self.cursor.fetchall()

    def close_db(self):
        self.conn.close()

    def get_all_users(self):
        return self.users

    def check_email_used(self, email):
        self.email = email
        query = """
            SELECT * FROM users WHERE email='%s'
        """ % (email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def user_signup(self, username, email, password, address, user_type):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.user_type = user_type
        
        user_credentials = {
            "username":self.username,
            "email":self.email,
            "password":self.password,
            "address":self.address,
            "user_type":self.user_type
        }
        email_check = self.check_email_used(user_credentials['email'])

        if email_check == []:
            reg_query = """
                INSERT INTO users (username, email, password, address, user_type) 
                VALUES ( %(username)s, %(email)s, %(password)s, %(address)s, %(user_type)s) 
                RETURNING user_id;
            """

            self.cursor.query(reg_query, user_credentials)
            user_id = self.cursor.fetchone()[0]
            self.conn.commit()
            self.close_db()
            return user_id
        else:
            raise BadRequest("Email is already in use")