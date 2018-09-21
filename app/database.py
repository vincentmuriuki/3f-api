from flask import current_app
import psycopg2
import os


# Local imports
from fastfoodfast import queries
from app.app import create_app

def init_databse():
    # Initiate the db
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    curr = conn.cursor()
    try:
        for query in queries:
            curr.execute()
        conn.commit()
        return conn
    except:
        print("Fail")

def dismantle():
    # Close db connections
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    
    conn.close()


init_databse()

