# System library
import os

# Third Party libraries
import psycopg2

# Local imports
from .fastfoodfast import queries
from instance.config import app_config

def db_type():
    """ Check the type of db used """
    if os.getenv("CONFIG_TYPE") == "testing":
        url = os.getenv("DATABASE_TEST_URL")
        return url
    else:
        url = os.getenv("DATABASE_URL")
        return url

def init_database():
    """ This method is used initialize database """
    url = db_type()
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    print("Connected to main db")
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        return conn
    except Exception as e:
        print(e)

    

def init_test_database():
    """ This method is used to initialize test database """
    url = db_type()
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    print("Connected to test db")
    dismantle()
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        return conn
    except Exception as e:
        print(e)
            

def dismantle():
    """ Destroy all data in table in the test database """
    url = os.getenv('DATABASE_TEST_URL')
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    meals = "DROP TABLE IF EXISTS meals CASCADE"
    orders = "DROP TABLE IF EXISTS orders CASCADE"
    category = "DROP TABLE IF EXISTS categories CASCADE"
    blacklist = "DROP TABLE IF EXISTS blacklist CASCADE"

    queries = [orders, meals, users, category, blacklist]
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
        

