import os

from flask import request
from werkzeug.exceptions import BadRequest

from app.api.v2.models.db_vars import Database
from app.api.v2.helpers.token import TokenGen

token_gen = TokenGen()

class OrderModels(Database):
    """ This will hold all order models """
    def __init__(self):
        super().__init__()
        
    def get_orders(self):
        """ Get orders made as a whole """
        self.cursor.execute("SELECT * FROM orders")
        result = self.cursor.fetchall()
        self.store()
        return result

    def get_order_by_id(self, order_id):
        """ Get an order by id """
        self.cursor.execute("SELECT * FROM orders WHERE order_id='%s'" % order_id)
        result = self.cursor.fetchone()
        self.store()
        return result

    def add_order(self, meal, qty, ordered_date, price, status, description, amount):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[0]
        else:
            auth_token = ''
            raise BadRequest("Token absences please ")

        user_id = token_gen.decode_auth_token(auth_token)
        
        self.cursor.execute("""
        INSERT INTO orders (user_id, meal, ordered_date, price, qty, amount, 
        status, description) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (user_id, meal, ordered_date, price, qty, amount, status, description))
        self.store()
        
    def update_status(self, order_id, status, delivered_date):
        """ Update an order is delivered """
        self.cursor.execute("""
        UPDATE orders SET status='%s' AND delivered_date='%s'
        WHERE order_id='%s'
        """ % (status, delivered_date,order_id))
        self.store()

    def find_order_by_user_id(self, user_id):        
        self.cursor.execute("SELECT * FROM orders WHERE user_id='%s'" % user_id)
        result = self.cursor.fetchall()
        self.store()
        return result

