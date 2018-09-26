import os

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, NotFound

from app.database import init_database

class UserModels(object):
    """ This class will hold all methods for user authentication """    
    def __init__(self):
        self.db = init_database()
        query  = """
            SELECT * FROM users 
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(query)
        self.users = self.cursor.fetchall()

    def get_login_email(self, email):
        query = "SELECT * FROM users WHERE email=?",(email,)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.db.close()
        return data

    def close_db(self):
        self.db.close()

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
        self.db.commit()
        self.db.close()
        return reject_token

    def check_email_used(self, email):
        self.email = email
        curr = self.db.cursor()
        curr.execute("SELECT email FROM users WHERE email = '%s'" % (self.email))
        result = curr.fetchone()
        print(result)
        if result:
            raise BadRequest("This email is already in use")
        status = True
        return status

    def user_signup(self,username, email, address, password, user_type = True):
        try:
            query = """INSERT INTO users (username, email, address, password, user_type) \
            VALUES (%s, %s, %s, %s, %s) RETURNING user_id"""

            curr = self.db.cursor()
            curr.execute(query, (username, email, address, password, user_type))
            user_id = curr.fetchone()[0]
            self.db.commit()
            self.db.close()
            return user_id
        except Exception as e:
            print(e)


        