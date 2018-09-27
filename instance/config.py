import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", '5PAVHUG4HuYaCjDvMTPBmnHV3bRamRxx')

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
    "default":Development
}