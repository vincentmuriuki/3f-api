from flask import request
import datetime as dt

class OrdersOperation:
    
    def __init__(self):
        self.orders = []

    def get_orders(self):
        return self.orders

    def order(
            self, order_id, username,
            product_name, product_price, 
            status, ordered_date, 
            delivered_date):
            
        self.name = product_name,
        self.price = product_price
        self.id = order_id
        self.username = username
        self.ordered_date = ordered_date
        self.delivered_date = delivered_date
        self.status = status

        self.order_fields = {
            "id":self.id,
            "username":self.username,
            "product_name":self.name,
            "product_price":self.price,
            "status":self.status,
            "ordered_date":self.ordered_date,
            "delivered_date":self.delivered_date
        }

    def get_specific_order(self, identifier):
        specific_order = [specific_order for specific_order in self.orders if specific_order['id'] == identifier]

        if specific_order:
           return specific_order
        else:
            return None 

    def save_order(self):
        data_json = request.get_json()
        new_order = {
            "id":len(self.orders) + 1,
            "username":data_json['username'],
            "product_name":data_json["product_name"],
            "product_price":data_json["product_price"],
            "status":"Pending",
            "ordered_date":str(dt.datetime.now()),
            "delivered_date":None
        }

        self.orders.append(new_order)
        return new_order



