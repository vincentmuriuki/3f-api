from .views import app, api, Orders

api.add_resource(Orders, '/api/v1/orders/<int:identifier>')
