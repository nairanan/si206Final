
from bs4 import BeautifulSoup
import sqlite3
import requests
import json
import re
import os
import unittest

pokemon_master_list = ["mesprit", 'sunkern', 'metang', 'barboach', 'victini', 'bronzor', 'roggenrola', 'floatzel', 
'keldeo', 'ledian', 'amaura', 'lugia', 'magby', 'galvantula', 'jellicent', 'machop', 'chatot', 'simisage', 'nidoking',
'tyranitar', 'arcanine', 'hippopotas', 'passimian', 'ludicolo', 'hakamo-o', 'crustle', 'armaldo', 'avalugg', 'archeops',
'gyarados', "pidgeot", "meloetta", 'leavanny', 'unfezant', 'mandibuzz', 'dusknoir', 'honedge', 'landorus', 'dratini',
'carrascosta', 'abomaasnow', 'abra', 'absol', 'aggron', 'aipom', 'altaria', 'amoonguss', 'castform', 'foongus', 'jumpluff',
 'croagunk', 'thundurus', 'aegislash', 'giratina', 'groudon', 'ho-oh', 'kyogre', 'salamence,']



def get_pokemon_tier(pokename):
    """
    Gets the tier for a pokemon from the smogon website. 
    Only accepts Pokemon with an official smogon tier (PU, NU, RU, UU, UUBL, OU, Uber)
    
    ARGUMENTS: 
        movie: pokemon name

    RETURNS:
        string of pokemon tier
    """
    url = 'https://www.smogon.com/dex/sm/pokemon/' + pokename + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup == None:
        print("Error: Pokemon not found")
    
    ul_tag = soup.find('ul', {'data-reactid': '.0.1.1.2.1.0:1.1.0.0.2.1.0'}) 
    tier = ul_tag.find('a')
    print(tier.text)
    return tier.text

    


def get_pokemon_stats(pokename):
    """
    Gets the stats of the given pokemon
    
    ARGUMENTS:
        pokemon name

    RETURNS:
        A dictionary of pokemon stats from PokeAPI
    
    """
    
    request = 'https://pokeapi.co/api/v2/pokemon/' + pokename + "/"
    details = requests.get(request)
    
    poke_details = details.json()
    stats_dict = {}
    if (poke_details == None):
        print("Error: Pokemon not found, please try again.")
        return None
    else:
        for stat in poke_details['stats']:
            value = stat['base_stat']
            name = stat["stat"]["name"]
            stats_dict[name] = stat
        return stats_dict


        
def setup_db():
    """
    Sets up database connection.

    ARGUMENTS: 
        None

    RETURNS:
        Database cursor and connection to database
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "Final_project.db")
    cur = conn.cursor()
    return cur, conn

def setup_tier_table(cur, conn):
    """
    Creates and updates the Tiers table in the database with new tiers

    ARGUMENTS
        database cursor and connection
    RETURNS
        None
        
    """
    tier_list = ['Uber', 'OU', 'UUBL', 'UU', 'RU', 'NU', 'PU']
    

    cur.execute("CREATE TABLE IF NOT EXISTS Tiers (id INTEGER PRIMARY KEY AUTOINCREMENT, tier TEXT UNIQUE)")

    for tier in tier_list:
        cur.execute("INSERT OR IGNORE INTO Tiers (tier) VALUES (?)", (tier, ))
    conn.commit()

def update_reviews_table(movie_dict, cur, conn):
    movie_title = movie_dict['Title']
    cur.execute('''SELECT id FROM Movies WHERE movie_title = ?''', (movie_title,))
    movie_id = cur.fetchone()[0]

    cur.execute('''CREATE TABLE IF NOT EXISTS Reviews (movie_id , imdb INTEGER,
     rotten_tomatoes INTEGER, metacritic INTEGER)''')
    
    imdb_rating = movie_dict["Ratings"][0]["Value"].rstrip("/10")
    imdb_rating = int(float(imdb_rating) * 10)

    rotten_tom_rating = movie_dict["Ratings"][1]["Value"].rstrip("%")
    rotten_tom_rating = int(rotten_tom_rating)

    metacritic_rating = movie_dict["Ratings"][2]["Value"].rstrip("/100")
    metacritic_rating = int(metacritic_rating)
    cur.execute('''INSERT OR IGNORE INTO Reviews (movie_id, imdb, rotten_tomatoes, metacritic)
     VALUES (?,?,?,?)''', (movie_id, imdb_rating, rotten_tom_rating, metacritic_rating, ))
    conn.commit()


def main():
    print(len(pokemon_master_list))
    tier_dic = {}
    for pokemon in pokemon_master_list:
        tier = get_pokemon_tier(pokemon)
        tier_dic[tier] = tier_dic.get(tier, 0) + 1
    print(tier_dic)



if __name__ == '__main__':
    main()   