import requests
import sqlite3

# Function to fetch makeup products from Makeup API
def fetch_makeup_products(params=None):
    url = "http://makeup-api.herokuapp.com/api/v1/products.json"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT,
        product_type TEXT,
        price REAL,
        rating REAL,
        product_tags TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

# Function to batch insert data into SQLite database
def batch_insert_into_database(products):
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()

    for product in products:
        cursor.execute('''
        INSERT INTO products (id, brand, name, product_type, price, rating, product_tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.get('id', None),
            product.get('brand', None),
            product.get('name', None),
            product.get('product_type', None),
            product.get('price', None),
            product.get('rating', None),
            ','.join(product.get('product_tags', []))
        ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create database and table
    create_database()

    # Define search parameters
    params = {
    'limit': 100
}

    # Fetch makeup products
    makeup_products = fetch_makeup_products(params=params)
    
    if makeup_products:
        # Insert fetched data into database
        batch_insert_into_database(makeup_products)
        print("Data inserted successfully!")
    else:
        print("No data fetched.")
