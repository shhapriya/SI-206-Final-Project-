import requests
import json
import unittest
import os
import sqlite3

def read_api_key (file):
    try:
        with open('api_key_lastfm.txt', 'r') as file:
            api_key = file.readline().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: {'api_key.txt'} not found.")
        return None
API_KEY = read_api_key("api_key_lastfm.txt")
API_URL = "https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key=API_KEY&format=json"


params = {
    "method": "chart.getTopArtists",
    "api_key": API_KEY,
    "format": "json"
}

def get_api_data (params):
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
    # Process the JSON response
        top_artists = data['artists']['artist']
        for artist in top_artists:
            print(artist['name'])
    else:
        print(f"Error {response.status_code}: {response.text}")

def set_up_datrabase (db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect('lastfm_data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS top_artists
                  (id INTEGER PRIMARY KEY, name TEXT, playcount INTEGER)''')

# Insert data into SQLite database
    # # for artist in top_artists:
    #     name = artist['name']
    #     playcount = int(artist['playcount'])  # Assuming 'playcount' is an integer
    #     cur.execute("INSERT INTO top_artists (name, playcount) VALUES (?, ?)",
    #                (name, playcount))
    return cur, conn