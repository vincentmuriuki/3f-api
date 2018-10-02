import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = (os.getenv("SECRET_KEY") or '5PAVHUG4HuYaCjDvMTPBmnHV3bRamRxx')

class Development(Config):
    DEBUG = True
    TESTING = False

class Testing(Config):
    DEBUG = True
    TESTING = True

class Staging(Config):
    DEBUG = False
    TESTING = False

class Production(Config):
    DEBUG = False
    TESTING = False


app_config = {
    "development":Development,
    "testing":Testing,
    "production":Production,
    "staging":Staging,
    "default":Development,
    "dbUrl":"dbname='fastfoodfast' host='localhost' port='5432' user='postgres' password='1234'",
    "test_db_url":"dbname='fastfoodtest' host='localhost' port='5432' user='postgres' password='1234'"
}