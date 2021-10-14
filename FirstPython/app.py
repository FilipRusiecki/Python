from flask import Flask

import datetime

app = Flask(__name__)

@app.route("/")     ##register the / URL with the Flask web Server
def index():
    return datetime.datetime.now().ctime()      ##the HTTP response




@app.route("/hello")
def hello():
    return "hello from my web app. :)"



if __name__ == "__main__":
    app.run()





