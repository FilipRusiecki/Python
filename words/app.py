from flask import Flask, render_template, request, session
import random
from datetime import datetime
from collections import Counter
import DBcm




config = {
        'host' : '127.0.0.1',    #link to the site
        'database': 'worddb',    #change the board 
        'user': 'wordUser',  #change this to the online data base
        'password': 'wordpasswd', #change password
}


app = Flask(__name__)

srcwrd = ""
#SAVE_FILE = "dataleaders.txt"
@app.get("/")
@app.get("/home")
def display_rules():
    return render_template("home.html")



@app.route("/game")
def play_game():


#starttime = time.time()
    #starttime = datetime.now()
    #session ["start_time"] = starttime
  
    setup_txt_file()                                # Sets up the txt files
    sourceword = get_source_word()                  # Finds the sourceword from the big.txt file
   # global srcwrd
    session["source_word"] = sourceword
    #srcwrd = sourceword
    
    return render_template("game.html", source_word = sourceword)


 
@app.get("/log")
def the_failure():
    #process_data_from_log(m_ip,m_ip,m_browser,m_source,m_matches)
  #  the_resulttime = ""
   # the_ip= ""
  #  the_browser=""
   # the_srcwrd=""
   # the_guessWord=""    
    t_logs = getmyLogs()
    print(t_logs)
    #thislist =[the_resulttime,the_ip,the_browser,the_srcwrd,the_guessWord]
    #process_data_from_log(thislist[0],thislist[1],thislist[2],thislist[3],thislist[4])
    return render_template("log.html", myLogs = t_logs)
    #the_ip = ip, the_browser = bZrowser, the_sourceWord = srcwrd, the_matches = guessWord
       #(ip, browser, srcwrd, guessWord))  
       
       

@app.route("/results")
def the_results():
    #guess_word_input()
    srcwrd = session["source_word"]
    
   # starttime = session["start_time"]
    #endtime = datetime.now()
    #resulttime = endtime - starttime
   # resulttime = str(resulttime)  
    
    #print("You finished in" ,resulttime)

   # session ["result_time"] = resulttime
    game_core(srcwrd)

    return render_template("results.html")





@app.get("/top10")
def get_top_10():
    return render_template("top10.html")


def game_core(srcwrd):
    print(srcwrd)
    mainWord = Counter(srcwrd)   
    #guesswordList = []
    wordWrong = False
    wordRight = False
    wordMistake = False
    wordShort = False
    wordEqualToSource = False
    name = request.args.get("the_name")
    #ip = socket.gethostname()
    starttime = datetime.now()      #this doesnt work properly as it only execuses for a split second when game coore is random
                                    #tried using sessions for the time but sql was throwing errors for time 
    for x in range(7):
        guessWord = request.args.get("playerinput").split(" ")
        print(len(guessWord[x]))


    
    for guesses in range(7):                            
        guessWord = request.args.get("playerinput").split(" ")          
        print(guessWord)
        singleGuessWord = guessWord[guesses]
        guess = Counter(singleGuessWord)                                
        guess = guess - mainWord                                        
        mainWord = Counter(srcwrd)                                 
        
        if srcwrd == singleGuessWord:
            wordEqualToSource = True
        
        print(guess)
        print(type(singleGuessWord))
        
        if len(singleGuessWord) >= 4:
            with open("endWords.txt", "r") as sf:
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
                if bool(guess) == True: 
                    print("Your letters don't match")
                    wordWrong = True 
                if bool(guess) == False: 
                    print("You guessed correctly")
        else:
            wordShort = True
        
            
    



    duplicates = checkDupes(guessWord)

    if duplicates == True:
        print("You have a duplicate in your words")
    if wordMistake == True:
        print("One or more of your words are not correct")
    if wordShort == True:
        print("One or more words are less than 4 letters")
    if wordEqualToSource == True:
        print("One or more words are equal to the sourceword")
    
 
    #starttime = session["start_time"]
    #resulttime = session["result_time"]
    #resulttime = str(resulttime)  
    
   # print("You finished in" ,resulttime)
   
   
    endtime = datetime.now()
    resulttime = endtime - starttime
    resulttime = str(resulttime)  
    
    print("You finished in" ,resulttime)
   
   
   
    guessWord = ' '.join(guessWord)
    print(guessWord)
    
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(ip)
    
    browser = request.headers.get('User-Agent')
    
    push_the_data(resulttime, name, srcwrd, guessWord)
    push_the_log(ip, browser, srcwrd, guessWord)
    #process_data_from_log(resulttime,ip,browser,srcwrd,guessWord)
    print("===============")
    print(resulttime)
    print(ip)
    print(srcwrd)
    print(browser)
    print("===============")

    #thislist = [browser,ip]
   # print(thislist)
    #print(type(thislist))
   # with open(SAVE_FILE, "a") as sf:
    #    print(f"{resulttime}|{ip}|{browser}|{srcwrd}|{guessWord}", file=sf)
    
    
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





def push_the_data(resulttime,name,srcwrd,guessWord):
    SQL = """
            insert into wordtable
            (time, name, sourceword, matches)
            value
            (%s, %s, %s, %s)
    
    """
    
    with DBcm.UseDatabase(config) as db:
        db.execute(SQL, (resulttime, name, srcwrd, guessWord))
        
        
        
        
        
def push_the_log(ip,browser,srcwrd,guessWord):
    SQL = """
            insert into wordlog
            (ip, browser, sourceword, matches)
            value
            (%s, %s, %s, %s)
    
    """
    
    with DBcm.UseDatabase(config) as db:
        db.execute(SQL, (ip, browser, srcwrd, guessWord))  



                                                                    #tried process the data from the log to be used in/logs
def process_data_from_log(the_resulttime,the_ip,the_browser,the_srcwrd,the_guessWord):
    with DBcm.UseDatabase(config) as db:
        SQL = """
                select time, ip, browser, sourceword, matches
                from wordlog
                order by time desc
              """
        db.execute(SQL)
        logs = db.fetchall()
       # thislist = [resulttime,ip,browser,srcwrd,guessWord]        
        #where = logs.index((thislist)) + 1
       # where = []
       # the_resulttime = session["result_time"]
        where = logs.index((the_resulttime,the_ip,the_browser,the_srcwrd,the_guessWord))+ 1
        #how_many = len(logs)
        return where,logs[:10]



    
def getmyLogs():
    with DBcm.UseDatabase(config) as db:
        SQL = """
            select *
            from wordlog
            order by time desc
        """
        db.execute(SQL)
        logs = db.fetchall()
    
    return logs

 #####################################################REFERENCE
def process_data(the_score, the_player):
    with DBcm.UseDatabase(config) as db:
        SQL = """
    select name, score
    from board
    order by score desc
    """
    db.exceute(SQL)
    scores = db.fetchall()
    where = scores.index((the_player, the_score)) + 1
    how_many = len(scores)
    
    return where, how_many, scores[:10]
 
 #####################################################REFERENCE
 

app.secret_key = "c1v2b34nb4n5m67c5v6bnjfyr384m96mi8un7b"


if __name__ == "__main__":  # True if executed directly, False if imported.
    app.run(debug=True, host="0.0.0.0")
