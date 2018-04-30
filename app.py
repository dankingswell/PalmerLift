from flask import Flask , request, make_response, jsonify,url_for
from Flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash,  check_password_hash
from functools import wraps
import uuid
import datetime


app = Flask(__name__)



@app.route("/login",methods=["GET","POST"])
def login():
    pass

@app.route("/",methods=["GET"])
def index():
    pass

@app.route("/register", methods=["GET","POST"])
def register():
    pass




if __name__ == "__main__":
    app.run(debug=True)