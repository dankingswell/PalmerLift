from flask import Flask , request, make_response, jsonify,url_for,render_template,redirect
from app import app
import security
from Models.QueryTool import Query
import uuid
from functools import wraps


def requireToken(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        token = ""
        if not request.cookies.get("access_token"):
            return make_response(redirect("/login"), jsonify({"Message":"Token expired or not avalible please login"}))
        token = request.cookies.get("access_token")

        decoded =  security.CheckToken(token)
        if not decoded:
            return jsonify({"Message" : "Token invalid"})
        print(decoded)
        UserSearch = Query.User.Get(headers="public_id", content=decoded["public_id"])

        if not UserSearch:
            return jsonify({"Message":"User not found, token invalid"})
        return func(UserSearch,*args,**kwargs)
    return wrapper


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("loginform.html")

    if request.method == "POST":

        form = request.form

        if not form["username"] or not form["password"]:
            return jsonify({"Message":"Missing Fields please complete form"})
        
        userFromDB = Query.User.Get(headers="username" ,content=form["username"])

        if not userFromDB:
            return jsonify({"Message": "User not found."})
        
        userFromDB = userFromDB["Row 0"]


        if not security.CheckPassword(form["password"],userFromDB["password"]):
            return jsonify({"Message":"Password incorrect please enter a valid password"})

        resp = make_response(redirect("/"))
        resp.set_cookie("access_token", value=security.MakeToken(userFromDB))
        
        return resp
        


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("registerform.html")
    if request.method == "POST":
        form = request.form
        print([x for x in form.values()])
        if not form["Username"] or not form["Email"] or not form["Password"] or not form["Confirm-password"]:
            return jsonify({"Message":"form is missing mandatory fields"}),402
        if form["Password"] != form["Confirm-password"]:
            return jsonify({"Message":"passwords do not match"})

        existing_username_check = Query.User.Get(headers="username",content=form["Username"])
        existing_email_check = Query.User.Get(headers="email",content=form["Email"])
        
        if existing_email_check:
            return jsonify({"message":"user all ready exists with that email"})
        elif existing_username_check:
            return jsonify({"message":"user all ready exists with that username"})
        
        user_to_insert = {
            "Public_Id" : str(uuid.uuid4()),
            "Username" : form["Username"],
            "Password" : security.HashPassword(form["Password"]),
            "Email": form["Email"],
        }

        print(user_to_insert.values())

        to_insert = ",".join([x for x in user_to_insert.values()])

        Query.User.Insert(content=to_insert)
        
        return jsonify({"data":user_to_insert})


        

@app.route("/createworkout",methods=["GET","POST"])
def createworkout():
    pass

@app.route("/testinsert")
def testi():
    query = Query
    print(query)
    result = Query.User.Insert(content="UUID5,admin3,12345,admin5@palmerswole.com")
    print(result)
    return jsonify({"message":result})


@app.route("/testquery")
@requireToken
def testq(ActiveUser):
    query = Query()
    print(query)
    result = Query.User.Get(columns="*")
    print(result)
    return jsonify({"message":result})
