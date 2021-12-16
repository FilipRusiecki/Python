from flask import Flask, render_template, request, session
import random
from datetime import datetime
from collections import Counter

from data_utils import save_the_data, process_data

app = Flask(__name__)

srcwrd = ""

@app.get("/")
@app.get("/index")
def display_rules():
    return render_template("index.html", title="The 4 letter word game thing")



@app.route("/play")
def play_game():

    setup_txt_file()                                # Sets up the txt files
    sourceword = get_source_word()                  # Finds the sourceword from the big.txt file
    srcwrd = sourceword
    
    return render_template("play.html", title="Start thinking!", source_word = sourceword)




@app.route("/results")
def the_results():
    #guess_word_input()
    game_core(srcwrd)

    return render_template("results.html", title="Victory")

@app.post("/fail")
def the_failure():
    return render_template("fail.html", title="You Failed!")

@app.get("/top10")
def get_top_10():
    return render_template("top10.html", title="TOP 10")


@app.get("/score")
def display_score():
    score = random.randint(1, 100)
    session["current_score"] = score  # sets the session value for this browser.
    return render_template(
        "score.html",
        title="Here's your winning score",
        score=score,  # =random.randint(1, 100)
    )


@app.post("/savescore")
def save_the_score():
    """Get, Save, Process and Display the score data."""
    the_player = request.form["player"]  # From the HTML form.
    the_score = session[
        "current_score"
    ]  # Gets the session value for the current browser.

    save_the_data(the_player, the_score)
    (where, how_many, ordered) = process_data(the_score, the_player)

    return render_template(
        "results.html",
        title="Here is how you did",
        name=the_player,
        score=the_score,
        position=where,
        length=how_many,
        topten=ordered,
    )

def game_core(srcwrd):
    print(srcwrd)
    mainWord = Counter(srcwrd)   
    #guesswordList = []
    wordWrong = False
    wordRight = False
    wordMistake = False
    wordShort = False
    wordEqualToSource = False

    for x in range(7):
        guessWord = request.args.get("playerinput").split(" ")
        print(len(guessWord[x]))


    starttime = datetime.now()
    for guesses in range(7):                            
        guessWord = request.args.get("playerinput").split(" ")           # Creates a string that will store the guessWord
        print(guessWord)
        singleGuessWord = guessWord[guesses]
        guess = Counter(singleGuessWord)                                # Creates a counter which counts all the letters to check against the source word
        guess = guess - mainWord                                         # Checks if all the letters inside the source word, match the letters inside the guess word
        mainWord = Counter(srcwrd)                                   # Reassigns the source word to main word, so you can check the next word
        
        if srcwrd == singleGuessWord:
            wordEqualToSource = True
        
        print(guess)
        print(type(singleGuessWord))
        
        if len(singleGuessWord) >= 4:
            with open("final.txt", "r") as sf:
                for line in sf:
                    stripped_line = line.strip()
                    if stripped_line == singleGuessWord:
                        wordRight = True
                        break
                    else:
                        wordRight = False

            if wordRight == False:
                wordMistake = True
                print("The word is not real")
            if wordRight == True:
                print("it is found")
                wordRight = False
                if bool(guess) == True: # Checks if the guess word is empty, and if it isn't, the letters don't match
                    print("Your letters don't match")
                    wordWrong = True ## this will currently break out of the loop, if the word does not match
                if bool(guess) == False: # Checks if the guess word is empty, and if it is, then the letters match
                    print("You guessed correctly")
        else:
            wordShort = True
        
            
    endtime = datetime.now()

    resulttime = endtime - starttime
    resulttime = str(resulttime)
    print("You finished in" ,resulttime)

    duplicates = checkDupes(guessWord)

    if duplicates == True:
        print("You have a duplicate in your words")
    if wordMistake == True:
        print("One or more of your words are not correct")
    if wordShort == True:
        print("One or more words are less than 4 letters")
    if wordEqualToSource == True:
        print("One or more words are equal to the sourceword")



def get_source_word():
    with open("big.txt") as bf:
        myList = bf.read()
    myList = myList.split("\n")
    index = random.randrange(len(myList))
    sourceword = myList[index]
    print("sourceword is :" + myList[index])
    return sourceword

def setup_txt_file():
    with open('final.txt', "w") as fw:
        with open('small.txt',"w") as sf:
            with open("big.txt","w") as bf:
                with open("words.txt") as wf:
                    for w in wf:
                        if "'s" not in w:
                            print(w.strip().lower(), file = fw)
                            if len(w) > 7:
                                print(w.strip().lower(), file = bf)
                            else: 
                                print(w.strip().lower(),file = sf)


def checkDupes(guesswordList):
    if len(guesswordList) == len(set(guesswordList)):
        return False
    else:
        return True

app.secret_key = "c1v2b34nb4n5m67c5v6bnjfyr384m96mi8un7b"


if __name__ == "__main__":  # True if executed directly, False if imported.
    app.run(debug=True, host="0.0.0.0")