# BRONZER PY FILE

import requests
import sqlite3
import json
import os
import sys

# Function to fetch lipstick products from Makeup API
def fetch_bronzer_products():
    url = "http://makeup-api.herokuapp.com/api/v1/products.json"
    params = {'product_type': 'bronzer', 'limit': 25}  # Only lipstick products, limit to 25
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch bronzer products: {response.status_code}")
        return None

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mybronzer (
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
        if product.get('product_type') == 'bronzer':  # Check product_type before insertion
            # Check if product with the same id already exists in the database
            cursor.execute("SELECT COUNT(*) FROM mybronzer WHERE id = ?", (product.get('id'),))
            count = cursor.fetchone()[0]

            if count == 0:  # Only insert if product with the same id doesn't exist
                cursor.execute('''
                INSERT INTO mybronzer (brand_id, brand_name, name, price, currency)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    product.get('brand_id', None),
                    product.get('brand_name', None),
                    product.get('name', None),
                    #product.get('product_type', None),
                    product.get('price', None),
                    product.get('currency', None)
                ))
    
    conn.commit()
    conn.close()


def main():
    # Create database and table
    create_database()

    # Count the number of rows currently in the database
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mybronzer")
    current_row_count = cursor.fetchone()[0]
    conn.close()

    # Determine the remaining rows to reach 100
    remaining_rows = 100 - current_row_count

    if remaining_rows > 0:
        try:
            while remaining_rows > 0:
                # Fetch new batch of bronzer products
                bronzer_products = fetch_bronzer_products()
                print("Fetched bronzer products:", bronzer_products)  # Debugging print

                if bronzer_products:
                    batch_size = min(25, remaining_rows)
                    batch_insert_into_database(bronzer_products[:batch_size])
                    remaining_rows -= batch_size
                    print(f"{batch_size} rows inserted. {remaining_rows} rows remaining.")
                else:
                    print("No bronzer data fetched. Exiting...")
                    break
        except Exception as e:
            print("Error inserting data:", e)
    else:
        print("Database already contains 100 rows.")

if __name__ == "__main__":
    main()
