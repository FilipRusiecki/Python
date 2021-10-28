from flask import Flask, request, render_template

import datetime

app = Flask(__name__)


#@app.route("/")  ##register the / URL with the Flask web Server
#def index():
    #return datetime.datetime.now().ctime()  ##the HTTP response
            

@app.get("/")
def home_page():
    return render_template("home.html",
                            the_title = "Home")

@app.route("/personal")
def personal_page():
    return render_template("personal.html",
                            the_title = "Section about me!")
     

@app.route("/cv")
def cv_page():
    return render_template("cv.html",
                            the_title = "CV")
                            
@app.route("/games")
def games_page():
    return render_template("games.html",
                            the_title = "games")
                            
@app.route("/interests")
def interests_page():
    return render_template("interests.html",
                            the_title = "interests")
                            
@app.route("/warning")
def warning_page():
    return render_template("warning.html",
                            the_title = "warning")

#@app.post("/processform")
#def process_form():
#   the_name = request.form["thename"]
#    the_dob = request.form["thedob"]
#   with open("suckers.txt", "a") as sf:
#        print (f"{the_name},{the_dob}", file=sf)
#    return f"Hi there, {the_name} we know you were bon on :{the_dob}. "

if __name__ == "__main__":
    app.run(debug=True)
