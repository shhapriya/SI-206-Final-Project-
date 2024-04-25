# Name: Nethra Vijayakumar
import requests
import json
import unittest
import os
import sqlite3
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize Spotipy with OAuth2 authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="84c4c33c4693466f985310abe2bf7abb",
                                               client_secret="875adb71f2d343478342fcdc58f85f27",
                                               redirect_uri= "http://localhost:8888/callback",
                                               scope="user-library-read"))

def connect_to_database(db):
   conn = sqlite3.connect(db)
   cur = conn.cursor()
   return conn, cur

def create_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS Songs (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    artist TEXT,
                    album TEXT,
                    release_year INTEGER,
                    length INTEGER,
                    popularity INTEGER
                )''')

def insert_song(cur, conn, name, artist, album, release_year, length, popularity):
    cur.execute('''INSERT INTO Songs (name, artist, album, release_year, length, popularity) 
                   VALUES (?, ?, ?, ?, ?, ?)''', (name, artist, album, release_year, length, popularity))
    conn.commit()

def fetch_and_insert_songs(cur, conn):
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        release_year = int(track['album']['release_date'][:4])
        length = track['duration_ms'] // 1000  # Convert milliseconds to seconds
        popularity = track['popularity']
        insert_song(cur, conn, name, artist, album, release_year, length, popularity)

def main():
   db_path = 'songs.db'
   conn, cur = connect_to_database(db_path)
   create_table(cur)
   playlistid = 'YOUR_PLAYLIST_ID_HERE'
   fetch_and_insert_songs(cur, conn, playlistid)
   conn.close()

if __name__ == "__main__":
    main()