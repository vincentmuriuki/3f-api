# System library
import os

# Third Party libraries
import psycopg2

# Local imports
from .fastfoodfast import queries

def init_database():
    """ This method is used initialize database """
    url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    print("Connected")
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        return conn
    except Exception as e:
        print(e)

def init_test_database():
    """ This method is used to initialize test database """
    url = os.environ.get("DATABASE_TEST_URL")
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
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
    users = "DROO TABLE IF EXISTS users CASCADE"
    meals = "DROP TABLE IF EXISTS meals CASCADE"
    orders = "DROP TABLE IF EXISTS orders CASCADE"
    category = "DROP TABLE IF EXISTS category CASCADE"

    queries = [orders, meals, users, category]
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(e)


init_database()
        

