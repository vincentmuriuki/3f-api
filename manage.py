import psycopg2 as p 
import os

from app.api.v2.models.users import UserModels
from app.api.v2.models.category import CategoryModels 
from app.api.v2.models.menu import MenuModels
from app.api.v2.models.orders import OrderModels
from fastfoodfast import queries        

class Table_Manipulation(object):

    def __init__(self):
        try:
            if os.getenv("DATABASE_TEST_URL") == "testing":
                self.conn = p.connect(
                    os.getenv('DATABASE_TEST_URL')
                    )
            else:
                self.conn = p.connect(os.getenv("DATABASE_URL"))
        except (Exception, p.DatabaseError) as error:
            print(error)

        
        print("connected")
        self.curr = self.conn.cursor()

    def create_tables_to_be_used(self):
        for query in queries:
            self.curr.execute(query)

        self.conn.commit()
        #self.curr.close()

    def drop(self):
        if os.getenv("CONFIG_TYPE") == "testing":
            users = "DROP TABLE IF EXISTS users"
            category = "DROP TABLE IF EXISTS categories"
            meals = "DROP TABLE IF EXISTS meals"
            orders = "DROP TABLE IF EXISTS orders"
            blacklist = "DROP TABLE IF EXISTS blacklist"
            queries = [users, category, meals, orders, blacklist]

            for query in queries:
                self.curr.execute(query)
                print("Dropped query: {}".format(query))

            self.conn.commit()
            #self.curr.close()
        else:
            self.create_tables_to_be_used()



db = Table_Manipulation()

if __name__ == "__main__":
    db.drop()
    db.create_tables_to_be_used()