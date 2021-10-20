from flask import Flask, request, render_template

import datetime

app = Flask(__name__)


@app.route("/")  ##register the / URL with the Flask web Server
def index():
    return datetime.datetime.now().ctime()  ##the HTTP response


@app.route("/hello")
def hello():
   ## 1 / 0 
    return "hello from my web app."
                        

@app.get("/home")
def home_page():
return render_template("home.html"
                        the_title="Welcome")



@app.get("/showform")
def display_form():
return render_template("form.html"
                            the_title="give details")


@app.post("/processform")
def process_form():
    the_name = request.form["thename"]
    the_dob = request.form["thedob"]
    with open("suckers.txt", "a") as sf:
        print (f"{the_name},{the_dob}", file=sf)
    return f"Hi there, {the_name} we know you were bon on :{the_dob}. "

if __name__ == "__main__":
    app.run(debug=True)
