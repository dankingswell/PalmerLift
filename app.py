from flask import Flask , request, make_response, jsonify,url_for
from Flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash,  check_password_hash
from functools import wraps
import uuid
import datetime


app = Flask(__name__)





@app.route("/")
def index():
    pass

if __name__ == "__main__":
    app.run(debug=True)