# System library
import os

# Third Party libraries
#from flask import current_app
import psycopg2

# Local imports
from .fastfoodfast import queries

def init_databse():
    # Initialize db
    url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(url)
    curr = conn.cursor()
    try:
        for query in queries:
            curr.execute(query)
        conn.commit()
        return conn
    except Exception as e:
        print(e)

def dismantle():
    # Close db connections
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    
    conn.close()


init_databse()

