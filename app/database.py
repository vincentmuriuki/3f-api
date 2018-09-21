from flask import current_app
import psycopg2
import os
from app import create_app

def init_databse():
    # Initiate the db
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    return conn

def dismantle():
    # Close db connections
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    
    conn.close()



