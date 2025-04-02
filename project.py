
from bs4 import BeautifulSoup
import sqlite3
import requests
import json
import re
import os
import unittest
import spotipy

API_KEY_omdb = "8a34795a"


#request = 'http://www.omdbapi.com/?t=' + movie + "&apikey=" + API_KEY

def get_list_of_songs(movie):
    """
    Gets the list of songs for a movie from soundtrack.net the website and
    returns it as a list .
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
    movie = movie.replace(" ", "+")
    request = 'http://www.omdbapi.com/?t=' + movie + "&apikey=" + API_KEY_omdb
    details = requests.get(request)
    
    movie_details = details.json()
    if (movie_details['Response'] == 'False'):
        print("Error: Movie not found on OMDB, please try again.")
        return None
    else:
        return movie_details


def main():
    print(get_list_of_songs("Guardians of the Galaxy"))
    print(get_movie_json("Guardians of the Galaxy"))

if __name__ == '__main__':
    main()   