# FOUNDATION PY FILE

import requests
import sqlite3
import json
import os
import sys


# Function to fetch foundation products from Makeup API
def fetch_foundation_products():
   url = "http://makeup-api.herokuapp.com/api/v1/products.json"
   params = {'product_type': 'foundation', 'limit': 25}  # Only foundation products, limit to 25
   response = requests.get(url, params=params)
  
   if response.status_code == 200:
       return response.json()
   else:
       print(f"Failed to fetch foundation products: {response.status_code}")
       return None


# Function to create SQLite database and table
def create_database():
   conn = sqlite3.connect('makeup.db')
   cursor = conn.cursor()
  
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS myfoundation (
       brand_id INTEGER PRIMARY KEY,
       brand_name TEXT,
       name TEXT,
       price DOUBLE,
       currency_name TEXT
   )
   ''')
  
   conn.commit()
   conn.close()


# Function to batch insert data into SQLite database
def batch_insert_into_database(products):
   conn = sqlite3.connect('makeup.db')
   cursor = conn.cursor()


   for product in products:
       if product.get('product_type') == 'foundation':  # Check product_type before insertion
           # Check if product with the same id already exists in the database
           cursor.execute("SELECT COUNT(*) FROM myfoundation WHERE id = ?", (product.get('id'),))
           count = cursor.fetchone()[0]


           if count == 0:  # Only insert if product with the same id doesn't exist
               cursor.execute('''
               INSERT INTO myfoundation (brand_id, brand_name, name, price, currency)
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




