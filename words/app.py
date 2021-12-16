from flask import Flask, request, render_template
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

def currentGivenWord(given):
    givenWord = given
    return givenWord

  
@app.get("/game")
def game_play():
    with open('smallWords.txt',"w") as sf:
        with open("bigWords.txt","w") as bf:
            with open("words.txt") as wf:
                with open("endWord.txt" , "w") as ff:
                    for w in wf:
                        if "'s" not in w:
                            print(w.lower().strip,file = ff)
                        if len(w) > 7:
                            print(w.lower().strip(), file = bf)
                        else: 
                            print(w.lower().strip(),file = sf)
                        
    with open ("bigWords.txt") as bigWordsList:
        givenWords = bigWordsList.read()
    
    global givenWord
    givenWord = (random.choice(givenWords.split()))

    return render_template("game.html",
                            the_title="play game", given_word = givenWord)
                            
with open ("endWord.txt") as fullList:
    wordlist = fullList.read()
    
    
@app.route("/processwords")
def score_page():
  #  with open ("bigWords.txt") as bigWordsList:
   #     givenWords = bigWordsList.read()
   # givenWord = (random.choice(givenWords.split()))


    playerWords = request.args.get("words.txt").split() #    playerWords = request.args.getlist(open("words.txt"))#.split()
    #word_list = playerWords.split()
    duplicateCounter = 0
    wordCounter = 0
    valid = True
    sevenWords = True
    acceptedWords = True

    for word in playerWords:
    #    if playerWords is None:
         #   print('List is None')
        wordCounter = wordCounter + 1
        if word.lower() not in wordlist:
            print("Not a real word!")
            outputMessage = "One or more words does not exist"
            acceptedWords = False
        if word.lower() == givenWord:           ##givenword and not word_list
            print("Player input the given word")
            outputMessage = "Player has input the given"
            acceptedWords = False
            sevenWords = False
        if len(word) < 4:                                             #Checking the word is 4 characters and more 
            print ("One or more words are shorter than 4 characters")
            outputMessage = "One or more words are shorter than 4 characters!"
            acceptedWords = False
            sevenWords = False
        else:
            for word in playerWords:
                for secondWord in playerWords:
                    if word.lower() == secondWord.lower():
                        duplicateCounter= duplicateCounter +1
                        
            if duplicateCounter > 7:
                print("dupe words :", playerWords)
                outputMessage = "dupe words"
                sevenwords = False


        lettersInGiven = Counter(givenWord)         ##change word list to givenWord
        print(lettersInGiven)


        if sevenWords == True:
            for word in playerWords:
                lettersInPlayer = Counter(word.lower())
                print("Player", lettersInPlayer)
                for i in lettersInPlayer:
                    if(lettersInPlayer[i] <= lettersInGiven[i]):
                        print("word is valid")
                        outputMessage = "valid word"
                    else:
                        print("not valid word")
                        valid = False
                        break
                        
            if valid == False:
                outputMessage = "some words are not valid"
                
                
        return render_template("processwords.html",                     ##word_lisst needs to be givenWord
                                the_title="proces words", given_word = givenWord , input_words = playerWords , validity = outputMessage ) 
            

@app.get("/top10")
def top10_page():
    return render_template("top10.html",
                        the_title="")


@app.get("/log")
def log_page():
    return render_template("log.html",
                        the_title="")



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
