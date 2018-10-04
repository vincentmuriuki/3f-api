import os 
import json

from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed
from flask import request

from app.api.v2.models.db_vars import Database

class CategoryModels(Database):
    def __init__(self):
        """ This is the model for the menu which holds all meals """
        super().__init__()

    def create_category(self, category_name):
        self.cursor.execute("INSERT INTO categories (category_name) VALUES ('%s')" % (category_name))
        self.store()

    def get_specific_category(self, category_name):
        self.cursor.execute("SELECT * FROM categories WHERE category_name='%s'" % category_name)
        found_category = self.cursor.fetchone()[1]
        self.store()
        return found_category
    
    def get_all_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        categories = self.cursor.fetchall()
        return categories