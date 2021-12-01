import DBcm

#dont forget to install dbcm on server client
config ={
    'host' : '1270.0.1',    #link to the site
    'database': 'worddb',    #change the board 
    'user': 'wordUser',  #change this to the online data base
    'password': 'wordpasswd', #change password
}


def save_the_data(name, score):
    with DBcm.UseDatabase(config) as db:
            db.execute(SQL, (name, score))
    SQL = """
    insert into board
    (name, score)
    values
    (%s, %s)
    """
   



    with open(SAVE_FILE, "a") as sf:
        print(f"{name}|{score}", file=sf)
           
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
    




   # with open(SAVE_FILE) as sf:
    #    data = sf.readlines()
 
    return where, how_many, scores[:10]