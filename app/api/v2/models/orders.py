from flask import request
from werkzeug.exceptions import BadRequest

from app.database import init_database
from app.api.v2.helpers.token import TokenGen

token_gen = TokenGen()

class OrderModels(object):
    """ This will hold all order models """

    def __init__(self):
        self.db = init_database()

    def get_orders(self):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM orders")
        result = curr.fetchall()
        self.db.commit()
        return result

    def get_order_by_id(self, order_id):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM orders WHERE order_id='%s'" % order_id)
        result = curr.fetchone()
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

        curr = self.db.cursor()
        curr.execute("""
        INSERT INTO orders (user_id, meal, ordered_date, price, qty, amount, 
        status, description) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (user_id, meal, ordered_date, price, qty, amount, status, description))
        self.db.commit()
        

