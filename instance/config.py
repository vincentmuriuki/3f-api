import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = (os.getenv("SECRET_KEY") or '5PAVHUG4HuYaCjDvMTPBmnHV3bRamRxx')
    DATABASE_URL = (os.getenv("DATABASE_URL"))

class Development(Config):
    DEBUG = True
    TESTING = False

class Testing(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URL = (os.getenv("DATABASE_TEST_URL"))

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