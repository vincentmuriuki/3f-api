from flask import request
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest, NotFound
from flask_restful import Resource
import psycopg2

from app.api.v2.models.category import CategoryModels
from app.api.v2.helpers.helpers import check_admin, auth_required
from app.api.v2.validators.validators import Validators

validator = Validators()
category_models = CategoryModels()

class Categories(Resource):
    """ This class houses all endpoints involving categories """
    @check_admin
    def get(self):
        data = category_models.get_all_categories()
        data = validator.check_no_items(data)
        return (
            {
                "status":"Success",
                "categories":data
            }
        ), 200
    @check_admin
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'category_name',
            type=str,
            required=True,
            help="Enter the category name"
        )
        args = parser.parse_args()
        category_name = args['category_name']
        try:
            check_results = category_models.get_specific_category(category_name)
            if check_results:
                raise BadRequest("A category of the name exists already")                
            category_models.create_category(category_name)   
        
            return (
                {
                    "status":"Success",
                    "message":"Category: {}, has been created".format(category_name)
                }
            ), 201   
        except Exception as e:
            print(e)

    @check_admin
    def delete(self):
        pass

    @check_admin
    def put(self):
        pass