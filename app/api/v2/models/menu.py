import json
import os

from app.api.v2.models.db_vars import Database

class MenuModels(Database):
    """ This is the model for the menu which holds all meals """
    def __init__(self):
        super().__init__()

    def delete_menu_table(self):
        """ Delete the menu of the user """
        self.delete_table("meals")    
    
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

    

    


    
