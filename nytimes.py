import requests
import json
import os
import sqlite3
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
#     cur.execute(
#         '''CREATE TABLE IF NOT EXISTS BestSellers (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT,
#             author TEXT,
#             isbn TEXT UNIQUE,
#             list_name TEXT,
#             date TEXT
#         )'''
#     )

def create_table(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS BestSellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT UNIQUE,
            list_name TEXT,
            date TEXT
        )'''
    )

def fetch_last_retrieved(cur):
    cur.execute("SELECT date FROM BestSellers ORDER BY date DESC LIMIT 1")
    last_retrieved = cur.fetchone()
    if last_retrieved:
        return last_retrieved[0]
    else:
        return None

def fetch_top_books(API_URL, params):
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)

def insert_best_sellers_books(cur, list_name, books_data, date):
    total_items = 0
    for book_info in books_data:
        title = book_info['title']
        author = book_info['author']
        isbn = book_info['isbn']
        try:
            cur.execute("INSERT INTO Bestsellers (Date, Year, Month, ISBN) VALUES (?, ?, ?, ?)",
                        (date, int(date.split('-')[0]), int(date.split('-')[1]), isbn))
            total_items += 1
        except sqlite3.IntegrityError:  # Handle duplicate entries
            pass
    return total_items


def main():
    conn, cur = connect_to_database('top_books.db')
    create_table(cur)
    
    API_KEY = read_api_key('api_key_nytimes.txt')
    
    # List of years you want to fetch data for
    years = ['2024', '2023', '2022', '2021', '2020']  # Add or remove years as needed
    
    for year in years:
        API_URL = f'https://api.nytimes.com/svc/books/v3/lists/{year}-01-01/hardcover-fiction.json'
        params = {'api-key': API_KEY}
        
        top_books_data = fetch_top_books(API_URL, params)
        
        list_name = "Hardcover Fiction"
        books_data = top_books_data['results']['books']
        
        insert_count = insert_best_sellers_books(cur, start_date, list_name, books_data)

        
    conn.commit()
    conn.close()

    # conn, cur = connect_to_database('top_books.db')
    # create_table(cur)

    # Fetching the current date for the list
    # import datetime
    # current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # API_URL = f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json'
    # params = {'api-key': read_api_key('api_key_nytimes.txt')}
    # top_books_data = fetch_top_books(API_URL, params)

    # # Check if data is retrieved successfully
    # if 'results' in top_books_data:
    #     list_name = "Hardcover Fiction"
    #     books_data = top_books_data['results']['books']
        
    #     # Inserting data into the table
    #     insert_best_sellers_books(cur, list_name, books_data, current_date)
        
    # else:
    #     print("Error: Unable to fetch top books data.")
    
    # conn.commit()
    # conn.close()

if __name__ == "__main__":
    main()

