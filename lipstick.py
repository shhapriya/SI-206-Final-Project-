import requests
import sqlite3


# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lipstick (
        id INTEGER PRIMARY KEY,
        brand TEXT,
        name TEXT,
        price DOUBLE,
        currency TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def batch_insert_into_database(products):
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()

    for product in products:
        # Check if the ID already exists in the database
        cursor.execute("SELECT COUNT(*) FROM lipstick WHERE id = ?", (product.get('id'),))
        count = cursor.fetchone()[0]

        if count == 0:  # Only insert if product with the same id doesn't exist
            # Handle None price by setting it to 0.0
            price = float(product.get('price', 0)) if product.get('price') is not None else 0.0
            
            cursor.execute("INSERT INTO lipstick (id, brand, name, price, currency) VALUES (?, ?, ?, ?, ?)",
                           (product.get('id', None),
                            product.get('brand', None),
                            product.get('name', None),
                            price,
                            product.get('currency', None)))

    conn.commit()
    conn.close()


def fetch_lipstick_products(page):
    url = "http://makeup-api.herokuapp.com/api/v1/products.json"
    params = {'product_type': 'lipstick', 'limit': 25, 'page': page}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch lipstick products: {response.status_code}")
        return None
def main():
    # Create database and table (existing code)
    create_database()

    # Fetch the last inserted ID from the database
    conn = sqlite3.connect('makeup.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM lipstick")
    last_id = cursor.fetchone()[0]
    conn.close()

    # Check if last_id is None and set it to 0 if so
    if last_id is None:
        last_id = 0

    # Determine the starting page number based on the last_id
    page = (last_id // 25) + 1

    # Track total inserted items
    total_inserted = 0

    while total_inserted < 100:
        # Fetch and insert products
        lipstick_products = fetch_lipstick_products(page)
        if lipstick_products:
            batch_insert_into_database(lipstick_products)
            total_inserted += len(lipstick_products)
            print(f"{total_inserted} rows inserted so far.")
        else:
            print("No more products found.")
            break  # Exit the loop if no products are returned
        page += 1  # Move to the next page

    print(f"Total of {total_inserted} lipstick products inserted.")

if __name__ == "__main__":
    main()


