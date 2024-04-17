# Name: Dhara Patel
# Email: dharajp@umich.edu
# shazam py file

import requests
import json
import unittest
import os
import sqlite3
from bs4 import BeautifulSoup

# USE beautiful soup for this 
# do requests.get
# read from
# create database



def create_database():
    conn = sqlite3.connect('shazam_top_200.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS songs
                 (rank INTEGER, title TEXT, artist TEXT)''')
    conn.commit()
    conn.close()

def insert_song(rank, title, artist):
    try:
        conn = sqlite3.connect('shazam_top_200.db')
        c = conn.cursor()
        c.execute("INSERT INTO songs VALUES (?, ?, ?)", (rank, title, artist))
        conn.commit()
        conn.close()
        print(f"Inserted: Rank: {rank}, Title: {title}, Artist: {artist}")
    except sqlite3.Error as e:
        print("Error inserting data:", e)

def scrape_shazam_top_200_US():
    url = 'https://www.shazam.com/charts/top-200/united-states'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the container holding the song information
        song_container = soup.find('ol', class_='charttracks')
        
        if song_container:
            # Extract song information from each list item
            for item in song_container.find_all('li', class_='overflow-hidden'):
                rank = int(item.find('div', class_='shz-col shz-col--rank').text.strip())
                title = item.find('div', class_='shz-col shz-col--track').text.strip()
                artist = item.find('div', class_='shz-col shz-col--artist').text.strip()
                
                # Insert song into database
                insert_song(rank, title, artist)
        else:
            print("Couldn't find song container.")
    else:
        print("Failed to retrieve webpage.")


def main():
    # Create database
    create_database()

    # Scrape and insert top 200 US songs
    scrape_shazam_top_200_US()

if __name__ == "__main__":
    main()