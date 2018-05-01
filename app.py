from flask import Flask , request, make_response, jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash,  check_password_hash
from functools import wraps
import uuid
import datetime


app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

from routes import *



if __name__ == "__main__":
    app.run(debug=True)