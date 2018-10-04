import datetime as dt
import os 

from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2 as p 

from flask import current_app


class Database:
    """ Holds all related details to the database """

    def __init__(self):
        if os.getenv("CONFIG_TYPE") =="testing":
            self.db_url = os.getenv("DATABASE_TEST_URL")
        else:
            self.db_url = os.getenv("DATABASE_URL")

        self.conn = p.connect(self.db_url)
        self.cursor = self.conn.cursor()

    def store(self):
        """ method to commit to the database """
        self.conn.commit()

    def close_connection(self):
        """ method to close database connection """
        self.cursor.close()


    