import json

from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from app.database import init_database

class Menu(object):
    """ This is the model for the menu which holds all meals """
    def __init__(self):
        self.db = init_database()

    def check_meal_exists(self, meal):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM meals WHERE name='%s'" % meal)
        result = curr.fetchone()
        self.db.commit()
        return result

    def get_menu(self):
        curr = self.db.cursor()
        curr.execute("SELECT * FROM meals")
        result = curr.fetchall()
        self.db.commit()
        return result

    def add_meal(self, name, description, price, category_name):
        curr = self.db.cursor()
        curr.execute("""
        INSERT INTO meals (name, description, price, category_name) \
        VALUES ('%s', '%s', '%s', '%s')
        """ % (name, description, price, category_name))
        self.db.commit()

    


    
