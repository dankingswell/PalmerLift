from flask import Flask
from werkzeug import generate_password_hash,  check_password_hash
from functools import wraps
import uuid
import datetime
import security
import Models 

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
from routes import *



if __name__ == "__main__":
    app.run()