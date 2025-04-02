
from bs4 import BeautifulSoup
import sqlite3
import requests
import json
import re
import os
import unittest
import spotipy

API_KEY_omdb = "8a34795a"




def get_list_of_songs(movie):
    """
    Gets the list of songs for a movie from the website soundtrack.net and
    returns it as a list.append
    
    ARGUMENTS: 
        movie: movie title

    RETURNS:
        a list of songs from the movie's soudntrack


    
    """
    movie = movie.lower()
    movie = movie.replace(" ", "-")
    
    
    #gets soup object
    url = 'https://www.soundtrack.net/movie/' + movie + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if soup == None:
        print("Error: Movie not found on sountrack.net. Please try again.")

    
    songs = []
    
    #gets song titles
    for item in soup.find_all('span', class_='songtitle'):
        song = item.text 
        songs.append(song.lower())
    
    return songs

def get_movie_json(movie):
    """
    Gets the details of the input movie from OMDB's api with an API request.
    Returns a dictionary of the movie details.
    
    ARGUMENTS:
        movie: movie title

    RETURNS:
        A dictionary version of the json response from OMDB API
    
    """
    movie = movie.replace(" ", "+")
    request = 'http://www.omdbapi.com/?t=' + movie + "&apikey=" + API_KEY_omdb
    details = requests.get(request)
    
    movie_details = details.json()
    if (movie_details['Response'] == 'False'):
        print("Error: Movie not found on OMDB, please try again.")
        return None
    else:
        #writes into a json file and returns a dictionary of info
        # file = open(movie + '.json', 'w')
        # json.dump(movie_details, file)
        # file.close()
        #movie_dict = json.loads(movie_details)
        return movie_details
        
def setup_db():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "Final_project.db")
    cur = conn.cursor()
    return cur, conn

def update_movies_table(movie_dict, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Movies (id INTEGER PRIMARY KEY AUTOINCREMENT, movie_title TEXT UNIQUE)")
    cur.execute("INSERT OR IGNORE INTO Movies (movie_title) VALUES (?)", (movie_dict['Title'],))
    conn.commit()



def main():
    movie = input('Please enter a movie name: ')
    print(get_list_of_songs(movie))
    movie_dict = get_movie_json(movie)
    cur, conn = setup_db()
    update_movies_table(movie_dict, cur, conn)



if __name__ == '__main__':
    main()   