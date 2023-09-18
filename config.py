# set your app config here
class DevConfig(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "hlky299dnp10eskj"
    FLASK_SECRET = SECRET_KEY
    MONGO_URI = "mongodb://localhost:27017/users"


class ProductionConfig(object):
    DEVELOPMENT = False
    DEBUG = False
    SECRET_KEY = "hlky299dnp10eskj"
    FLASK_SECRET = SECRET_KEY
    MONGO_URI = "mongodb://localhost:27017/users"
