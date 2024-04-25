# NYTIMES PY FILE

import requests
import json
import os
import sqlite3
import sys

from datetime import datetime

#import time

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

def create_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS BestSellers_A (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT UNIQUE,
            publisher TEXT,
            list_name TEXT
        )'''
    )

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
        isbn = book_info['primary_isbn10']
        publisher = book_info['publisher']

        #price = book_info.get('price', 0.0)  # Default to 0.0 if price is not available
        try:
            cur.execute("INSERT INTO BestSellers_A (title, author, publisher, isbn, list_name) VALUES (?, ?, ?, ?, ?)",
                        (title, author, publisher, isbn, list_name))
            total_items += 1
        except sqlite3.IntegrityError:  # Handle duplicate entries
            pass
    return total_items


def main():
    conn, cur = connect_to_database('top_books_new_two.db')
    create_table(cur)
    cur.execute("SELECT COUNT(*) FROM BestSellers_A")
    existing_count = cur.fetchone()[0]

    API_KEY = read_api_key("api_key_nytimes.txt")
    years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017']
    total_items = existing_count

    for year in years:
        API_URL = f'https://api.nytimes.com/svc/books/v3/lists/{year}-01-01/hardcover-fiction.json'
        params = {'api-key': API_KEY}
        top_books_data = fetch_top_books(API_URL, params)

        list_name = "Hardcover Fiction"
        books_data = top_books_data.get('results', {}).get('books', [])

        for book_info in books_data:
            title = book_info['title']
            author = book_info['author']
            isbn = book_info['primary_isbn10']
            publisher = book_info['publisher']

            cur.execute("SELECT COUNT(*) FROM BestSellers_A WHERE isbn=?", (isbn,))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO BestSellers_A (title, author, publisher, isbn, list_name) VALUES (?, ?, ?, ?, ?)",
                            (title, author, publisher, isbn, list_name))
                total_items += 1

            if total_items >= existing_count + 25:
                break

        if total_items >= existing_count + 25:
            break

    conn.commit()
    conn.close()
    print("Data stored in SQLite database successfully!")

if __name__ == "__main__":
    main()
