from flask import Flask, render_template, request, session

app = Flask(__name__)

from data_utils import save_the_data, process_data

import random


@app.get("/")
@app.get("/score")
def display_score():
   score=random.randint(1,100)
   session["current_score"] = score #sets the session value for this browser
   return render_template("score.html", title="the big score", score=score#=random.randint(1, 100
   )


@app.post("/savescore")
def save_score():
    """
        1. Get the game and the score from the form
        2. Save the data to storage
        3. Generate a response to send to the use
            a.  Confirm score with player
            b.  Display the top ten previous scores
            c.  Tell the player where they ended up on the list
            
    """
    the_player = request.form["player"]   #from the HTML form
   # the_score = request.form["score"]   #from HTML hidden tag
    the_score = session["current_score"]   #gets the session value for the current browser
    
    
    save_the_data(the_player, the_score)
    
    with open(SAVE_FILE, "a") as sf:
        print(f"{the_player} | {the_score}", file=sf)
  
    
        
    where,how_many,ordered = process_data(the_score, the_player)
  
  
    return render_template (
        "results.html",
        title ="here is who you are",
        name=the_player,
        score=the_score,
        position=where,
        length=how_many,
        topten=ordered,
    )
    
    return f"{the_player}, {the_score},ok"
app.secret_key =":) dshbadhsbadhbshbsai1203i2109eokm3$ %^YTHDFDE$%TRHGFDVFE$T%RGFDRR "
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
