import json

def go():
    with open('games.json') as f:
        config = json.load(f)
    
    return config