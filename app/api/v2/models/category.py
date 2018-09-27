import os 
import json

from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed
from flask import request

from app.database import init_database

class CategoryModels(object):
    def __init__(self):
        self.db = init_database()

    def create_category(self, category_name):
        curr = self.db.cursor()
        curr.execute("INSERT INTO categories (category_name) VALUES ('%s')" % category_name)
        self.db.commit()

    def get_specific_category(self, category_name):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM categories WHERE category_name='%s'" % category_name)
        found_category = curr.fetchone()[1]
        self.db.commit()
        return found_category

    def get_all_categories(self):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM categories")
        categories = curr.fetchall()
        return categories