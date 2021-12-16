from flask import Flask, request, render_template
from data_utils import save_the_data, process_data
import datetime
import random                      #HERE WE IMPORT THE RANDOM

from collections import Counter    #IMPORTING THE COUNTER
from datetime import datetime      #WE IMPORT THIS TO CHECK FOR TIME  

app = Flask(__name__)


##@app.route("/")  ##register the / URL with the Flask web Server
##def index():
##    return datetime.datetime.now().ctime()  ##the HTTP response


##@app.route("/hello")
##def hello():
   ## 1 / 0 
##    return "hello from my web app."
                        

@app.get("/home")
def home_page():
    return render_template("home.html",
                        the_title="")


@app.get("/top10")
def top10_page():
    return render_template("top10.html",
                        the_title="")


@app.get("/log")
def log_page():
    return render_template("log.html",
                        the_title="")

@app.get("/game")
def display_form():
    return render_template("game.html",
                            the_title="play game")

@app.post("/results")
def results_page():
    return render_template("results.html",
                        the_title="")

@app.get("/loose")
def loose_page():
    return render_template("loose.html",
                        the_title="")
if __name__ == "__main__":
    app.run(debug=True)
