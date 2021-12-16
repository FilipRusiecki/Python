from flask import Flask, request, render_template
from data_utils import save_the_data, process_data
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

    setup_txt_file()
    sourceword = get_source_word()


    game_core(sourceword)

    return render_template("game.html",
                            the_title="play game", source_word = sourceword)





def game_core(sourceword):
    mainWord = Counter(sourceword)
    guesswordList = []
    wordWrong = False
    wordRight = False
    wordMistake = False
    wordShort = False
    wordEqualToSource = False


    starttime = datetime.now()
    for guesses in range(7):                           
        guessWord = input("Enter Words:")              # Creates a string that will store the guessWord
        guesswordList.append(guessWord)                # Adds to the end of the list which contains all the guess words
        guess = Counter(guessWord)                     # Creates a counter which counts all the letters to check against the source word
        guess = guess - mainWord                       # Checks if all the letters inside the source word, match the letters inside the guess word
        mainWord = Counter(sourceword)                 # Reassigns the source word to main word, so you can check the next word
        
        processWord = request.args.get("playerInput").split()
        if sourceword == guessWord:
            wordEqualToSource = True
        
        if len(guessWord) >= 4:
            with open("endWords.txt", "r") as sf:
                for line in sf:
                    stripped_line = line.strip()
                    if stripped_line == guessWord:
                        wordRight = True
                        break
                    else:
                        #print("One or more of your words are not correct")
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
                    break;
                if bool(guess) == False: # Checks if the guess word is empty, and if it is, then the letters match
                    print("You guessed correctly")
        else:
            wordShort = True
        
            
    endtime = datetime.now()

    resulttime = endtime - starttime
    resulttime = str(resulttime)
    print("You finished in" ,resulttime)

    duplicates = checkDupes(guesswordList)

    if duplicates == True:
        print("You have a duplicate in your words")
    if wordMistake == True:
       # print("One or more of your words are not correct")
        if wordShort == True:
            print("One or more words are less than 4 letters")
    if wordEqualToSource == True:
        print("One or more words are equal to the sourceword")



def get_source_word():
    with open("bigWords.txt") as bf:
        myList = bf.read()
    myList = myList.split("\n")
    index = random.randrange(len(myList))
    sourceword = myList[index]
    print("sourceword is :" + myList[index])
    return sourceword

def setup_txt_file():
    with open('endWords.txt', "w") as fw:
        with open('smallWords.txt',"w") as sf:
            with open("bigWords.txt","w") as bf:
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

    
    
def checkDupes(guesswordList):
    if len(guesswordList) == len(set(guesswordList)):
        duplicates = False
    else:
        duplicates = True




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
