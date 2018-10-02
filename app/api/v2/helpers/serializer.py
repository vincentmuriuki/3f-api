class Serializers:
    """ This will convert results from a database to a dictionary to be loaded to json"""
    def __init__(self):
        pass

    def serialize_order(self, value):
        data = {}
        data["order_id"] = value[0]
        data["user_id"] = value[1]
        data["meal"] = value[2]
        data["ordered_date"] = value[3]
        data["delivered_date"] = value[4]
        data["price"] = value[5]
        data["qty"] = value[6]
        data["amount"] = value[7]
        data["status"] = value[8]
        data["description"] = value[9]

        return data

    def serialize_orders(self, orders):
        
        for u in orders:
            order = self.serialize_order(u)
            data = []
            data.append(order)
            return order
        

    
