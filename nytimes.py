# Name: Dhara Patel
# Email: dharajp@umich.edu
# ny times py file

import requests
import json
import unittest
import os
import sqlite3
from bs4 import BeautifulSoup
import sys

def read_api_key(file_name):
    try:
        with open(file_name, 'r') as file:
            api_key = file.readline().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return None

def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    return conn, cur

# def create_table(cur):
#     cur.execute('''CREATE TABLE IF NOT EXISTS BestSellersLists (
#         list_id INTEGER PRIMARY KEY,
#         title TEXT,
#         first_published TEXT,
#         last_published TEXT)
#     ''')

def create_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS BestSellersList(
        book_id INTEGER PRIMARY KEY,
        list_name TEXT,
        title TEXT,
        author TEXT,
        isbn TEXT)''')

def fetch_last_retrieved(cur):
    cur.execute("SELECT list_name FROM BestSellersLists ORDER BY list_id DESC LIMIT 1")
    last_retrieved = cur.fetchone()
    if last_retrieved:
        return last_retrieved[0]
    else:
        return ''

def fetch_top_books(API_URL, params):
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)

def insert_best_sellers_books(cur, list_name, books_data):
    total_items = 0
    for book_info in books_data:
        title = book_info['title']
        author = book_info['author']
        isbn = book_info['isbn']
        try:
            cur.execute("INSERT INTO BestSellersLists (list_name, title, author, isbn) VALUES (?, ?, ?, ?)",
                        (list_name, title, author, isbn))
            total_items += 1
        except sqlite3.IntegrityError:  # Handle duplicate entries
            pass
    return total_items

def main():
    conn, cur = connect_to_database('top_books.db')
    create_table(cur)
    # Assuming you have the API URL and parameters defined somewhere
    API_URL = 'https://api.nytimes.com/svc/books/v3/lists/2024-01-01/hardcover-fiction.json'
    params = {'api-key': read_api_key('api_key_nytimes.txt')}
    top_books_data = fetch_top_books(API_URL, params)
    last_retrieved_list = fetch_last_retrieved(cur)
    if last_retrieved_list:
        # Do something with the last retrieved list
        pass
    # Assuming you have the list name and books data obtained from the API
    list_name = "Hardcover Fiction"
    books_data = top_books_data['results']['books']
    insert_best_sellers_books(cur, list_name, books_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
