import os

from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from flask_restful import Resource, reqparse
from flask import request

from app.api.v2.models.menu import MenuModels
from app.api.v2.helpers.helpers import check_admin
from app.api.v2.validators.validators import Validators

validator = Validators()
menu_models = MenuModels()

class Menu(Resource):
    """ This class holds the endpoints for meals """
    def get(self):
        menu = menu_models.get_menu()
        menu = validator.check_no_items(menu)
        return (
            {
                "menu":menu
            }
        ), 200

    @check_admin
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'product_name',
            type=str,
            required=True,
            help="A product must have a name"
        )
        parser.add_argument(
            'description',
            type=str,
            required=True,
            help="A product description is required to explain more on the meal"
        )
        parser.add_argument(
            'price',
            type=int,
            required=True,
            help="A meal must have a price"
        )
        parser.add_argument(
            'category_name',
            type=str,
            required=True,
            help="A meal must have a category"
        )
        args = parser.parse_args()
        result = menu_models.check_meal_exists(args['product_name'])
        if result:
            raise BadRequest("This meal already exists: {}".format(args['product_name']))
        
        menu_models.add_meal(
            args['product_name'], args['description'],
            args['price'], args['category_name']
        )

        return (
            {
                "status":"Success",
                "message":"Meal added to menu",
                "meal":args
            }
        )