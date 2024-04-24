import requests
import json
import os
import sqlite3
import sys


def read_api_key(file):
   try:
       with open('api_key_lastfm.txt', 'r') as f:
           api_key = f.readline().strip()
           return api_key
   except FileNotFoundError:
       print(f"Error: {'api_key_lastfm.txt'} not found.")
       return None



def connect_to_database(database_name):
   conn = sqlite3.connect(database_name)
   cur = conn.cursor()
   return conn, cur




def create_top_tracks_table(cur):
   cur.execute('''
       CREATE TABLE IF NOT EXISTS top_tracks (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           Name TEXT,
           Playcount INTEGER,
           Listeners INTEGER,
           artistID INTEGER
       )
   ''')




def fetch_top_tracks(API_URL, params):
   response = requests.get(API_URL, params=params)
   if response.status_code == 200:
       return response.json()
   else:
       print(f"Error {response.status_code}: {response.text}")
       sys.exit(1)




def insert_top_tracks(cur, tracks_data):
   total_items = 0
   for track in tracks_data:
       name = track['name']
       playcount = int(track['playcount'])
       listeners = int(track['listeners'])
       artist_name = track['artist']['name']


       # Insert artist if not exists
       cur.execute('''
           INSERT OR IGNORE INTO top_artists (name)
           VALUES (?)
       ''', (artist_name,))


       # Fetch artist's id
       cur.execute('SELECT id FROM top_artists WHERE name = ?', (artist_name,))
       artist_id = cur.fetchone()


       if artist_id:
           artist_id = artist_id[0]  # Directly assign the integer value


       # Insert track
       try:
           cur.execute('''
               INSERT INTO top_tracks (Name, Playcount, Listeners, artistID)
               VALUES (?, ?, ?, ?)
           ''', (name, playcount, listeners, artist_id))
           total_items += 1
       except sqlite3.IntegrityError:
           pass


   return total_items




def main():
   # Connect to SQLite database
   conn, cur = connect_to_database('lastfm_data.db')


   # Create top tracks table
   create_top_tracks_table(cur)


   # Get the total count of existing items in the database
   cur.execute("SELECT COUNT(*) FROM top_tracks")
   existing_count = cur.fetchone()[0]


   # API parameters
   API_KEY = read_api_key("api_key_lastfm.txt")
   API_URL = "https://ws.audioscrobbler.com/2.0/"
   method = "chart.getTopTracks"
   limit = 50  # Number of results per page
   total_items = existing_count  # Initialize total items counter
   page = 1  # Initialize page number


   params = {
       "method": method,
       "api_key": API_KEY,
       "format": "json",
       "limit": limit,
       "page": page  # Fetch the first page initially
   }


   response_data = fetch_top_tracks(API_URL, params)


   if 'tracks' in response_data and 'track' in response_data['tracks']:
       while total_items < (existing_count + 25):
           print(total_items)


           tracks_data = response_data['tracks']['track']


           # Insert 25 tracks at a time
           total_tracks_inserted = insert_top_tracks(cur, tracks_data[:25])
           print(f"Inserted {total_tracks_inserted} new tracks into top_tracks table.")


           cur.execute("SELECT COUNT(1) FROM top_tracks")
           total_tracks = cur.fetchone()[0]


           if total_tracks >= existing_count + 25:
               break


           page += 1  # Increment page for the next batch
           params['page'] = page
           response_data = fetch_top_tracks(API_URL, params)


   else:
       print("Error: Unable to fetch top tracks data.")


   conn.commit()
   conn.close()
   print("Data stored in SQLite database successfully!")




if __name__ == "__main__":
   main()
