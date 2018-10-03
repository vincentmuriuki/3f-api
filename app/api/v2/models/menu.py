import json
import os

from app.database import init_database, init_test_database

class MenuModels(object):
    """ This is the model for the menu which holds all meals """
    def __init__(self):
        if os.getenv("CONFIG_TYPE") == "testing":
            self.db = init_test_database()
        else:
            self.db = init_database()

        self.curr = self.db.cursor()

    def check_meal_exists(self, meal):
        self.curr.execute("SELECT * FROM meals WHERE name='%s'" % meal)
        result = self.curr.fetchone()
        self.db.commit()
        return result

    def get_menu(self):
        self.curr = self.db.cursor()
        self.curr.execute("SELECT * FROM meals")
        result = self.curr.fetchall()
        self.db.commit()
        return result

    def add_meal(self, name, description, price, category_name):
        self.curr = self.db.cursor()
        self.curr.execute("""
        INSERT INTO meals (name, description, price, category_name) \
        VALUES ('%s', '%s', '%s', '%s')
        """ % (name, description, price, category_name))
        self.db.commit()

    


    
