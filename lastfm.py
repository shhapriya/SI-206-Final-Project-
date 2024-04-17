import requests
import json
import os
import sqlite3
import sys


def read_api_key (file):
   try:
       with open('api_key_lastfm.txt', 'r') as file:
           api_key = file.readline().strip()
           return api_key
   except FileNotFoundError:
       print(f"Error: {'api_key.txt'} not found.")
       return None
  
def connect_to_database(database_name):
   conn = sqlite3.connect(database_name)
   cur = conn.cursor()
   return conn, cur


def create_table(cur):
   cur.execute('''CREATE TABLE IF NOT EXISTS top_artists
                  (id INTEGER PRIMARY KEY, name TEXT UNIQUE, playcount INTEGER)''')


def fetch_last_retrieved(cur, total_items):
   cur.execute("SELECT name FROM top_artists ORDER BY id DESC LIMIT 1 OFFSET ?", (total_items,))
   last_retrieved = cur.fetchone()
  
   if last_retrieved:
       return last_retrieved[0]
   else:
       return ''


def fetch_top_artists(API_URL, params):
   response = requests.get(API_URL, params=params)
  
   if response.status_code == 200:
       return response.json()
   else:
       print(f"Error {response.status_code}: {response.text}")
       sys.exit(1)


def insert_top_artists(cur, top_artists):
   total_items = 0
   for artist in top_artists:
       name = artist['name']
       playcount = int(artist['playcount'])  # Assuming 'playcount' is an integer
       try:
           cur.execute("INSERT INTO top_artists (name, playcount) VALUES (?, ?)",
                       (name, playcount))
           total_items += 1
       except sqlite3.IntegrityError:  # Handle duplicate entries
           pass
   return total_items




def main():
    # Connect to SQLite database
    conn, cur = connect_to_database('lastfm_data.db')

    # Create table (if it doesn't exist)
    create_table(cur)

    # Get the total count of existing items in the database
    cur.execute("SELECT COUNT(*) FROM top_artists")
    existing_count = cur.fetchone()[0]

    # API parameters
    API_KEY = read_api_key("api_key_lastfm.txt")
    API_URL = "https://ws.audioscrobbler.com/2.0/"
    method = "chart.getTopArtists"
    limit = 25  # Number of results per page
    total_items = existing_count  # Initialize total items counter

    while total_items < existing_count + 25:  # Fetch only 25 new items each time
        params = {
            "method": method,
            "api_key": API_KEY,
            "format": "json",
            "limit": limit,
            "page": 1  # Always fetch the first page
        }

        response_data = fetch_top_artists(API_URL, params)
        
        if 'artists' in response_data and 'artist' in response_data['artists']:
            top_artists = response_data['artists']['artist']

            for artist in top_artists:
                name = artist['name']
                playcount = int(artist['playcount'])  # Assuming 'playcount' is an integer

                # Check if the artist is new and not already in the database
                cur.execute("SELECT COUNT(*) FROM top_artists WHERE name=?", (name,))
                if cur.fetchone()[0] == 0:
                    try:
                        cur.execute("INSERT INTO top_artists (name, playcount) VALUES (?, ?)", (name, playcount))
                        total_items += 1
                    except sqlite3.IntegrityError:
                        # Handle duplicates
                        pass
        else:
            print("Error: Unable to fetch top artists data.")
            sys.exit(1)

        conn.commit()

    conn.close()
    print("Data stored in SQLite database successfully!")

if __name__ == "__main__":
    main()



if __name__ == "__main__":
   main()




  




# do top artists table first
#then when doing top tracks table, if the artists name exists, create an integer key
#check the artist name for eahc track, do a select statement, and see if it exists
# if it doesn't exist, then create a number -1


# SELECT ROWS
# top ar
#do subplots
# if both count listeners, compare
