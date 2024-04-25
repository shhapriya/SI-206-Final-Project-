# Name: Nethra Vijayakumar
import requests
import json
import unittest
import os
import sqlite3
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="84c4c33c4693466f985310abe2bf7abb",
                                               client_secret="875adb71f2d343478342fcdc58f85f27",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))

def connect_to_database(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    return conn, cur

def create_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS top100songs (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    artist TEXT,
                    album TEXT,
                    release_year INTEGER,
                    length INTEGER,
                    popularity INTEGER
                )''')

def insert_song(cur, conn, name, artist, album, release_year, length, popularity):
    cur.execute('''INSERT INTO top100songs (name, artist, album, release_year, length, popularity) 
                   VALUES (?, ?, ?, ?, ?, ?)''', (name, artist, album, release_year, length, popularity))
    conn.commit()


def fetch_and_insert_songs(cur, conn, playlist_url, offset):
    # Extract playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    
    try:
        # Fetch tracks from the specified playlist with the specified offset
        results = sp.playlist_tracks(playlist_id, limit=25, offset=offset)
        
        for idx, item in enumerate(results['items']):
            track = item['track']
            name = track['name']
            artist = track['artists'][0]['name']
            album = track['album']['name']
            release_year = int(track['album']['release_date'][:4])
            length = track['duration_ms'] // 1000  # Convert milliseconds to seconds
            popularity = track['popularity']
            insert_song(cur, conn, name, artist, album, release_year, length, popularity)
            
    except Exception as e:
        print(f"Error fetching tracks from the playlist: {e}")

def main():
    db_path = 'songs.db'
    conn, cur = connect_to_database(db_path)
    create_table(cur)
    playlist_url = 'https://open.spotify.com/playlist/6UeSakyzhiEt4NB3UAd6NQ?si=970c8c3a7d894fa4'
    
    offset = 0
    total_tracks = sp.playlist_tracks(playlist_url)['total']
    
    while offset < total_tracks:
        fetch_and_insert_songs(cur, conn, playlist_url, offset)
        offset += 25
    
    conn.close()

if __name__ == "__main__":
    main()