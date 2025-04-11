
from bs4 import BeautifulSoup
# from helium import *
from playwright.sync_api import sync_playwright
import sqlite3
import requests
import json
import re
import os
import unittest

pokemon_master_list = ["mesprit", 'victini', 'bronzor', 'floatzel', 'ledian', 'lugia', 'galvantula', 'jellicent', 'chatot', 'simisage', 'nidoking',
'tyranitar', 'arcanine', 'passimian', 'ludicolo', 'crustle', 'armaldo', 'avalugg', 'gyarados', "pidgeot", 'leavanny', 'unfezant', 'mandibuzz', 'dusknoir', 'landorus',
'carracosta', 'abomasnow', 'absol', 'aggron', 'altaria', 'amoonguss', 'castform', 'jumpluff', 'thundurus', 'aegislash', 'giratina', 'groudon', 'ho-oh', 'kyogre',
'salamence', 'azumarill', 'butterfree', 'cacturne', 'chesnaught', 'claydol', 'clefable', 'cloyster', 'combusken', 'golem', 'golduck', 'greninja', 'heatran', 'huntail',
'hydreigon', 'hypno', 'kommo-o', 'lycanroc', 'magearna', 'magnezone', 'manaphy', 'mawile', 'ninetales', 'oricorio', 'passimian', 'pelipper', 'pinsir', 'plusle',
'rapidash', 'rotom', 'sawsbuck', 'seaking', 'shaymin', 'silvally', 'slowbro', 'snorlax', 'steelix', 'swampert', 'swellow', 'tentacruel', 'torterra', 'vikavolt', 
'volcarona', 'weezing', 'xatu', 'zekrom', 'dragalge', 'gigalith', 'emolga', 'excadrill', 'drampa', 'diggersby', 'conkeldurr', 'honchkrow', 'hoopa', 'pikachu', 
'muk-alola', 'necrozma', 'nihilego', 'octillery', 'pawniard', 'phione', 'piloswine', 'jolteon', 'kabutops', 'hippowdon', 'haxorus', 'hawlucha', 'alomomola', 
'aerodactyl', 'ambipom', 'ampharos', 'araquanid', 'bewear', 'bronzong', 'celesteela', 'clawitzer', 'cresselia', 'diancie', 'druddigon']



def get_pokemon_tier(pokename):
    """
    Gets the tier for a pokemon from the smogon website. 
    
    ARGUMENTS: 
        pokemon: pokemon name

    RETURNS:
        string of pokemon tier
    """
    url = 'https://www.smogon.com/dex/sm/pokemon/' + pokename.lower() + '/'
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless = False  )
            page = browser.new_page()
            page.goto(url, wait_until = "domcontentloaded")
            html = page.inner_html('ul.FormatList')
            soup = BeautifulSoup(html, 'html.parser')
            tier = soup.find('a').text
            print(tier)
            return(tier)
        except TimeoutError:
            print(f"{pokename} not found on Smogon")
            return None

    


def get_pokemon_stats(pokename):
    """
    Gets the stats of the given pokemon
    
    ARGUMENTS:
        pokemon name

    RETURNS:
        A dictionary of pokemon stats from PokeAPI
    
    """
    try:
        request = 'https://pokeapi.co/api/v2/pokemon/' + pokename.lower() + "/"
        details = requests.get(request)
        poke_details = details.json()

    except ValueError:
        print(f"Could not find {pokename} on PokeAPI")
        return None

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
    conn = sqlite3.connect(path + "/" + "Pokemon_data.db")
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
    tier_list = ['Uber', 'OU', 'UUBL', 'UU', 'RU', 'NU', 'PU', 'ZU']
    

    cur.execute("CREATE TABLE IF NOT EXISTS Tiers (id INTEGER PRIMARY KEY AUTOINCREMENT, tier TEXT UNIQUE)")

    for tier in tier_list:
        cur.execute("INSERT OR IGNORE INTO Tiers (tier) VALUES (?)", (tier, ))
    conn.commit()

def update_stats_table(pokename, cur, conn):
    pokemon_tier = get_pokemon_tier(pokename)

    if pokemon_tier is None:
        return -1
        
    cur.execute('''SELECT id FROM Tiers WHERE tier = ?''', (pokemon_tier,))
    tier_id = cur.fetchone()[0]
    
    stats_dict = get_pokemon_stats(pokename)
    if stats_dict == None:
        return -1

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

    cur.execute('''CREATE TABLE IF NOT EXISTS Stats (tier_id , name TEXT UNIQUE,
     hp INTEGER, attack INTEGER, special_attack INTEGER, defense INTEGER,
     special_defense INTEGER, speed INTEGER)''')
    conn.commit()

    num_inserted = 0
    index = 0;
    while num_inserted < 25:
        cur.execute('''SELECT name FROM Stats WHERE name = ?''', (pokemon_master_list[index],))
        if cur.fetchone() == None:
            result = update_stats_table(pokemon_master_list[index], cur, conn)
            if result is not -1:
                num_inserted += 1
        index += 1
    conn.close()

    


if __name__ == '__main__':
    main()   