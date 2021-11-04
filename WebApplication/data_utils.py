
SAVE_FILE = "data/leaders.txt"

def save_the_data(name, score):
    with open(SAVE_FILE, "a") as sf:
        print(f"{name}|{score}", file=sf)
           
def process_data(the_score, the_player):
    with open(SAVE_FILE) as sf:
        data = sf.readlines()
  
    scores = []
    for row in data:
        name, score = row.strip().split("|")
        scores.append(f"{score} {name}")
        
    ordered = sorted (scores, reverse=True)
    where = ordered.index(f"{the_score} {the_player}")+1
    
    how_many = len(ordered)
    
    return where,