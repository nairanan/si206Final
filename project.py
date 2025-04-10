
from bs4 import BeautifulSoup
# from helium import *
from playwright.sync_api import sync_playwright
import sqlite3
import requests
import json
import re
import os
import unittest

pokemon_master_list = ["mesprit", 'victini', 'bronzor', 'floatzel', 'keldeo', 'ledian', 'lugia', 'galvantula', 'jellicent', 'chatot', 'simisage', 'nidoking',
'tyranitar', 'arcanine', 'passimian', 'ludicolo', 'crustle', 'armaldo', 'avalugg', 'gyarados', "pidgeot", 'leavanny', 'unfezant', 'mandibuzz', 'dusknoir', 'landorus',
'carracosta', 'abomasnow', 'absol', 'aggron', 'altaria', 'amoonguss', 'castform', 'jumpluff', 'thundurus', 'aegislash', 'giratina', 'groudon', 'ho-oh', 'kyogre',
'salamence', 'azumarill', 'butterfree', 'cacturne', 'chesnaught', 'claydol', 'clefable', 'cloyster', 'combusken', 'golem', 'golduck', 'greninja', 'heatran', 'huntail',
'hydreigon', 'hypno', 'kommo-o', 'lycanroc', 'magearna', 'magnezone', 'manaphy', 'mawile', 'ninetails', 'oricorio', 'passimian', 'pelipper', 'pinsir', 'plusle',
'rapidash', 'rotom', 'sawsbuck', 'seaking', 'shaymin', 'silvally', 'slowbro', 'snorlax', 'steelix', 'swampert', 'swellow', 'tentacruel', 'torterra', 'vikavolt', 
'volcarona', 'weezing', 'xatu', 'zekrom', 'dragalge', 'gigalith', 'emolga', 'excadrill', 'drampa', 'diggersby', 'conkeldurr', 'honchkrow', 'hoopa', 'pikachu']



def get_pokemon_tier(pokename):
    """
    Gets the tier for a pokemon from the smogon website. 
    Only accepts Pokemon with an official smogon tier (PU, NU, RU, UU, UUBL, OU, Uber)
    
    ARGUMENTS: 
        pokemon: pokemon name

    RETURNS:
        string of pokemon tier
    """
    url = 'https://www.smogon.com/dex/sm/pokemon/' + pokename.lower() + '/'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False  )
        page = browser.new_page()
        page.goto(url, wait_until = "domcontentloaded")
        html = page.inner_html('ul.FormatList')
        soup = BeautifulSoup(html, 'html.parser')
        tier = soup.find('a').text
        return(tier)

    


def get_pokemon_stats(pokename):
    """
    Gets the stats of the given pokemon
    
    ARGUMENTS:
        pokemon name

    RETURNS:
        A dictionary of pokemon stats from PokeAPI
    
    """
    
    request = 'https://pokeapi.co/api/v2/pokemon/' + pokename.lower() + "/"
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
            stats_dict[name] = value
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

def update_stats_table(pokename, cur, conn):
    pokemon_tier = get_pokemon_tier(pokename)
    cur.execute('''SELECT id FROM Tiers WHERE tier = ?''', (pokemon_tier,))
    tier_id = cur.fetchone()[0]

    cur.execute('''CREATE TABLE IF NOT EXISTS Stats (tier_id , name TEXT,
     hp INTEGER, attack INTEGER, special_attack INTEGER, defense INTEGER,
     special_defense INTEGER, speed INTEGER)''')
    
    stats_dict = get_pokemon_stats(pokename)

    hp = stats_dict["hp"]
    attack = stats_dict["attack"]
    sp_attack = stats_dict["special-attack"]
    defense = stats_dict["defense"]
    sp_defense = stats_dict["special-defense"]
    speed = stats_dict["speed"]

    cur.execute('''INSERT OR IGNORE INTO Stats (tier_id, name, hp, attack, special_attack, 
    defense, special_defense, speed) VALUES (?,?,?,?,?,?,?,?)''', 
    (tier_id, pokename, hp, attack, sp_attack, defense, sp_defense, speed,))
    conn.commit()


def main():
    cur, conn = setup_db()
    setup_tier_table(cur, conn)
    for pokemon in pokemon_master_list[0:10]:
        update_stats_table(pokemon, cur, conn)

    


if __name__ == '__main__':
    main()   