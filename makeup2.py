# MASCARA PY FILE

import requests
import sqlite3
import json
import os
import sys

# Function to fetch lipstick products from Makeup API
def fetch_mascara_products():
    url = "http://makeup-api.herokuapp.com/api/v1/products.json"
    params = {'product_type': 'mascara', 'limit': 25}  # Only lipstick products, limit to 25
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch mascara products: {response.status_code}")
        return None

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mymascara (
        brand_id INTEGER PRIMARY KEY,
        brand_name TEXT,
        name TEXT,
        price DOUBLE,
        currency TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

# Function to batch insert data into SQLite database
def batch_insert_into_database(products):
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()

    for product in products:
        if product.get('product_type') == 'mascara':  # Check product_type before insertion
            # Check if product with the same id already exists in the database
            cursor.execute("SELECT COUNT(*) FROM mymascara WHERE id = ?", (product.get('id'),))
            count = cursor.fetchone()[0]

            if count == 0:  # Only insert if product with the same id doesn't exist
                cursor.execute('''
                INSERT INTO mymascara (brand_id, brand_name, name, price, currency)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    product.get('brand_id', None),
                    product.get('brand_name', None),
                    product.get('name', None),
                    product.get('price', None),
                    product.get('currency', None),
                ))
    
    conn.commit()
    conn.close()


def main():
    # Create database and table
    create_database()

    # Count the number of rows currently in the database
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mymascara")
    current_row_count = cursor.fetchone()[0]
    conn.close()

    # Determine the remaining rows to reach 100
    remaining_rows = 100 - current_row_count

    # Fetch lipstick products
    mascara_products = fetch_mascara_products()

    if mascara_products:
        # Insert fetched data into database in batches of 25 until reaching 100 rows
        try:
            while remaining_rows > 0:
                batch_size = min(25, remaining_rows)
                batch_insert_into_database(mascara_products[:batch_size])
                remaining_rows -= batch_size
                print(f"{batch_size} rows inserted. {remaining_rows} rows remaining.")
        except Exception as e:
            print("Error inserting data:", e)
    else:
        print("No mascara data fetched.")

if __name__ == "__main__":
    main()


