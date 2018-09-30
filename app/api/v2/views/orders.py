from werkzeug.exceptions import BadRequest, NotFound
from flask_restful import Resource, Api

from app.api.v2.models.orders import OrderModels
from app.api.v2.helpers.helpers import auth_required

order_models = OrderModels()

class OrdersMain(Resource):
    """ This class holds the endpoints for orders as a whole """
    @auth_required
    def get(self):
        orders = order_models.get_orders()
        return (
            {
                "status":"Success",
                "orders":orders
            }
        ), 200

