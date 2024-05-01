import json
import os
import requests
import sqlite3

API_KEY = "13021dfb347b4592b5c6f6195b4f00e1"

def gather_player_data(cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS players (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT, 
                   birthCity TEXT, 
                   birthState TEXT, 
                   salary INTEGER,
                   weight INTEGER,
                   height INTEGER,
                   college TEXT)''')
    
    url = "http://archive.sportsdata.io/v3/nba/stats/json/players/2023-11-13-15-51.json"
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    response = requests.get(url, headers=headers)
    
    players_data = json.loads(response.content.decode('utf-8'))
    
    cur.execute("SELECT COUNT(name) FROM players")
    current_count = cur.fetchone()[0]
    
    new_players_count = 0
    
    print(f"Current number of players in database: {current_count}")
    
    for player in players_data:
        if new_players_count >= 25:
            break
        
        if player.get('BirthCountry') == "USA":
            name = player.get("FirstName", "") + " " + player.get("LastName", "")
            city = player.get("BirthCity", "")
            state = player.get("BirthState", "")
            salary = player.get("Salary", 0)
            weight = player.get("Weight", 0)
            height = player.get("Height", 0)
            college = player.get("College", "")
            
            # Check if player already exists in the database
            cur.execute("SELECT id FROM players WHERE name=?", (name,))
            existing_player = cur.fetchone()
            
            if existing_player:
                print(f"Player '{name}' already exists, skipping insertion.")
                continue
            
            # Insert new player into the database
            cur.execute('''INSERT INTO players (
                           name, birthCity, birthState, salary, weight, height, college) 
                           VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (name, city, state, salary, weight, height, college))
            
            if cur.rowcount > 0:
                new_players_count += 1
                print(f"Inserted player: {name}")
    
    conn.commit()
    print(f"Inserted {new_players_count} new players.")

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'complete.db')
    cur = conn.cursor()
    
    gather_player_data(cur, conn)
    
    cur.close()

if __name__ == "__main__":
    main()

