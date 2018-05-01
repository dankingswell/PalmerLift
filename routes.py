from app import app


@app.route("/login",methods=["GET","POST"])
def login():
    pass

@app.route("/",methods=["GET"])
def index():
    return "<h2>test</h2>"

@app.route("/register", methods=["GET","POST"])
def register():
    pass

@app.route("/createworkout",methods=["GET","POST"])
def createworkout():
    pass