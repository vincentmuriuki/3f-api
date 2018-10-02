from flask import request
from werkzeug.exceptions import BadRequest, NotFound
from flask_restful import Resource

from app.api.v2.models.category import CategoryModels
from app.api.v2.helpers.helpers import check_admin, auth_required

category_models = CategoryModels()

class Categories(Resource):
    """ This class houses all endpoints involving categories """
    @check_admin
    def get(self):
        data = category_models.get_all_categories()
        return (
            {
                "categories":data
            }
        ), 200
    @check_admin
    def post(self):
        data = request.get_json()
        category_name = data['category_name']
        try:
            check_results = category_models.get_specific_category(category_name)
            if check_results:
                raise BadRequest("A category of the name exists already")                
            category_models.create_category(category_name)
            return (
                {
                    "message":"Category: {}, has been created".format(category_name)
                }
            ), 201
        except Exception as e:
            raise BadRequest("Something just isnt right: {}".format(e))        

    @check_admin
    def delete(self):
        pass

    @check_admin
    def put(self):
        pass