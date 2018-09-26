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
        self.cursor.execute(query)
        self.users = self.cursor.fetchall()

    def get_login_email(self, email):
        query = "SELECT * FROM users WHERE email ='%s'" % (email)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.cursor.close()
        return data

    def close_db(self):
        self.conn.close()

    def get_all_users(self):
        return self.users

    def user_logout(self, token):
        """ This will handle the logging out of a user """
        query = """
            INSERT INTO blacklist VALUES
            (?) RETURNING user_tokens;
        """, (token)
        self.cursor.execute(query)
        reject_token = self.cursor.fetchone()[0]
        self.conn.commit()
        self.cursor.close()
        return reject_token

    def check_email_used(self, email):
        self.email = email
        query = """
            SELECT * FROM users WHERE email='%s'
        """ % (email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def user_signup(self, username, email, password, address, user_type=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.user_type = user_type
        email_check = self.check_email_used(self.email)

        if not email_check:
            reg_query = """
                INSERT INTO users VALUES ( ?, ?, ?, ?, ?) 
                RETURNING user_id;
            """, (
                self.username,
                self.email,
                self.password,
                self.address,
                self.user_type 
            )

            self.cursor.query(reg_query)
            user_id = self.cursor.fetchone()[0]
            self.conn.commit()
            self.close_db()
            return user_id
        else:
            raise BadRequest("Email is already in use")