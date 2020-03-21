from flask import Flask,url_for,request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world"


@app.route("/User/",methods=["GET","POST"])
def User():
    return f"User {request.method}"


@app.route("/Product")
def Product():
    return "Product"

@app.route("/File",methods=["POST"])
def File():
    for file in dict(request.files).values():
        print(file.filename)

    return "File"



with app.test_request_context():
    print(url_for("Product"))
    print(url_for("static",filename="style.css"))
