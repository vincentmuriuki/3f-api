import json
import os

from app.api.v2.models.db_vars import Database

class MenuModels(Database):
    """ This is the model for the menu which holds all meals """
    def __init__(self):
        super().__init__()  
    
    def check_meal_exists(self, meal):
        self.cursor.execute("SELECT * FROM meals WHERE name='%s'" % meal)
        result = self.cursor.fetchone()
        self.store()
        return result

    def get_menu(self):
        self.cursor.execute("SELECT * FROM meals")
        result = self.cursor.fetchall()
        self.store()
        return result

    def add_meal(self, name, description, price, category_name):
        self.cursor.execute("""
        INSERT INTO meals (name, description, price, category_name) \
        VALUES ('%s', '%s', '%s', '%s')
        """ % (name, description, price, category_name))
        self.store()

    

    


    
