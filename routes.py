from flask import Flask , request, make_response, jsonify,url_for,render_template,redirect,flash
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
            resp = redirect(url_for("login"),200)
            resp.headers["Message"] = "Token expired or not avalible please login"
            return resp

        token = request.cookies.get("access_token")

        decoded =  security.CheckToken(token)
        if not decoded:
            resp = redirect("/login")
            resp.headers["Message"] = "Token expired or is invalid please login"
            return resp

        UserSearch = Query.User.Get(headers="public_id", content=decoded["public_id"])

        if not UserSearch:
            return jsonify({"Message":"User not found, token invalid"})
        return func(UserSearch["Row 0"],*args,**kwargs)
    return wrapper



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("loginform.html")

    if request.method == "POST":

        form = request.form

        if not form["username"] or not form["password"]:
            resp = make_response(redirect("/login"))
            resp.headers["Message"] = "Please ensure all fields are completed"
            resp = security.InvalidateToken(resp)
            flash(flash(resp.headers["Message"]))
            return resp
        
        userFromDB = Query.User.Get(headers="username" ,content=form["username"])

        if not userFromDB:
            resp = make_response(redirect("/login"))
            resp.headers["Message"] = "User not found with those credentials, please check and resubmit your login information"
            resp = security.InvalidateToken(resp)
            flash(resp.headers["Message"])
            return resp
        
        userFromDB = userFromDB["Row 0"]


        if not security.CheckPassword(form["password"],userFromDB["password"]):
            resp = make_response(redirect("/login"))
            resp.headers["Message"] = "User not found with those credentials, please check and resubmit your login information"
            resp = security.InvalidateToken(resp)
            flash(resp.headers["Message"])
            return resp
            

        resp = make_response(redirect("/profile"))
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

        print("user to insert ",user_to_insert.values())

        to_insert = ",".join([x for x in user_to_insert.values()])

        Query.User.Insert(content=to_insert)
        
        return jsonify({"data":user_to_insert})


        

@app.route("/workouts",methods=["GET","POST"])
@requireToken
def workouts(ActiveUser):
    if request.method == "GET":
        return render_template("workouts.html")

    if request.method == "POST":
        data = request.get_json()
        print(data)
        return render_template("workouts.html")


    # exercises will be sent as JSON object in format:
    # workout:{
    #       exercise : {
    #           name:name,
    #           sets:amount, 
    #           set1:{
    #                    "Reps": x , weight: n 
    #                 },
    #           set2:{
    #                    "Reps": x , weight: n 
    #                 }
    #               }
    #          }





## MAKE GOALS DB
@app.route("/goals",methods=["GET","POST"])
@requireToken
def goals(ActiveUser):
    if request.method == "GET":
        goals= {
            "1":"icons8-biceps.png",
            "2":"icons8-barbell.png",
            "3":"icons8-bodybuilder.png",
            "4":"icons8-fitness.png",
            "5":"icons8-jumping-rope.png"
        }
        return render_template("goals.html",goals=goals)
    pass

@app.route("/progression",methods=["GET","POST"])
def progression():
    if request.method == "GET":
        return render_template("progression.html")
    pass



@app.route("/profile")
@requireToken
def profile(ActiveUser):
    print(ActiveUser)
    user_info = {
        "username" : ActiveUser.get("username"),
        "email":ActiveUser.get("email")
    }
    return render_template("profile.html",user=user_info)


# @app.route("/testinsert")
# def testi():
#     query = Query
#     print(query)
#     result = Query.User.Insert(content="UUID5,admin3,12345,admin5@palmerswole.com")
#     print(result)
#     return jsonify({"message":result})


# @app.route("/testquery")
# @requireToken
# def testq(ActiveUser):
#     query = Query()
#     print(query)
#     result = Query.User.Get(columns="*")
#     print(result)
#     return jsonify({"message":result})


@app.route("/Status")
@requireToken
def status(ActiveUser):
    if ActiveUser["username"]:
        return ActiveUser["username"], 202
    
    return None
