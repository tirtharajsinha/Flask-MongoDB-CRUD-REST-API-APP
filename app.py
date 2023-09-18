from flask_pymongo import PyMongo
from flask import Flask, abort
from flask_wtf.csrf import CSRFProtect
from userController import UserControler
import os

# Initializing Flask App
app = Flask(__name__)

# config
app.config.from_object("config.DevConfig")

# Setting up Mongo enviromnment
mongodb_client = PyMongo(app)
db = mongodb_client.db

# CSRF Protection(For now not required)
# csrf = CSRFProtect(app)

# Initializing user controller
Ucontroller = UserControler(db, app)
app = Ucontroller.getApp()


# Error handler
@app.errorhandler(404)
def page_not_found(error):
    abort(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=port)
