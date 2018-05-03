from flask import Flask , request, make_response, jsonify,url_for,render_template
from app import app
import security



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("loginform.html")
    if request.method == "POST":
        return url_for("/")

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("registerform.html")

@app.route("/createworkout",methods=["GET","POST"])
def createworkout():
    pass