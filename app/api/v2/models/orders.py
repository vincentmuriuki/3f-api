import os

from flask import request
from werkzeug.exceptions import BadRequest

from app.database import init_database, init_test_database
from app.api.v2.helpers.token import TokenGen

token_gen = TokenGen()

class OrderModels(object):
    """ This will hold all order models """

    def __init__(self):
        if os.getenv("CONFIG_TYPE") == "testing":
            self.db = init_test_database()
        else:
            self.db = init_database()

        self.curr = self.db.cursor()

    def get_orders(self):
        
        self.curr.execute("SELECT * FROM orders")
        result = self.curr.fetchall()
        self.db.commit()
        return result

    def get_order_by_id(self, order_id):
        
        self.curr.execute("SELECT * FROM orders WHERE order_id='%s'" % order_id)
        result = self.curr.fetchone()
        self.db.commit()
        return result

    def add_order(self, meal, qty, ordered_date, price, status, description, amount):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
            raise BadRequest("Token absences please ")

        user_id = token_gen.decode_auth_token(auth_token)

        
        self.curr.execute("""
        INSERT INTO orders (user_id, meal, ordered_date, price, qty, amount, 
        status, description) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (user_id, meal, ordered_date, price, qty, amount, status, description))
        self.db.commit()
        
    def update_status(self, order_id, status, delivered_date):
        
        self.curr.execute("""
        UPDATE orders SET status='%s' AND delivered_date='%s'
        WHERE order_id='%s'
        """ % (status, delivered_date,order_id))
        self.db.commit()

    def find_order_by_user_id(self, user_id):
        
        self.curr.execute("SELECT * FROM orders WHERE user_id='%s'" % user_id)
        result = self.curr.fetchall()
        self.db.commit()
        return result

