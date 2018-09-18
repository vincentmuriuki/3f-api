from .views import app, api, OrderManipulation

api.add_resource(OrderManipulation, '/api/v1/orders/<int:identifier>')
