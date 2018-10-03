import os 
import json

from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed
from flask import request

from app.database import init_database, init_test_database

class CategoryModels(object):
    def __init__(self):
        if os.getenv("CONFIG_TYPE") == "testing":
            self.db = init_test_database()
        else:
            self.db = init_database()

        self.curr = self.db.cursor()

    def create_category(self, category_name):
        self.curr = self.db.cursor()
        self.curr.execute("INSERT INTO categories (category_name) VALUES ('%s')" % (category_name))
        self.db.commit()

    def get_specific_category(self, category_name):
        self.curr = self.db.cursor()
        self.curr.execute("SELECT * FROM categories WHERE category_name='%s'" % category_name)
        found_category = self.curr.fetchone()[1]
        self.db.commit()
        return found_category
    
    def get_all_categories(self):
        self.curr = self.db.cursor()
        self.curr.execute("SELECT * FROM categories")
        categories = self.curr.fetchall()
        return categories