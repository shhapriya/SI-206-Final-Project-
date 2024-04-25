import requests
import sqlite3

# Function to connect to SQLite database
def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    return conn, cur

# Function to create CurrencyKeys table
def create_currency_keys_table(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS CurrencyKeys (
            currency_id INTEGER PRIMARY KEY,
            currency_name TEXT UNIQUE
        )
    ''')

# Function to populate CurrencyKeys table with unique currency values
def populate_currency_keys_table(cur, currency_names):
    for currency_name in currency_names:
        cur.execute('''
            INSERT OR IGNORE INTO CurrencyKeys (currency) VALUES (?)
        ''', (currency_name,))

def create_brand_keys_table(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS BrandKeys (
            id INTEGER PRIMARY KEY,
            brand TEXT UNIQUE
        )
    ''')

# Function to update a table to replace currency names with integer keys
def update_table_with_currency_keys(cur, table_name, currency_column_name):
    cur.execute(f'''
        UPDATE {table_name}
        SET {currency_column_name}_id = (
            SELECT id FROM CurrencyKeys WHERE CurrencyKeys.currency = {table_name}.{currency_column_name}
        )
    ''')

# Function to create BrandKeys table
def update_table_with_brand_keys(cur, table_name, brand_column_name):
    cur.execute(f'''
        UPDATE {table_name}
        SET {brand_column_name}_id = (
            SELECT id FROM BrandKeys WHERE BrandKeys.brand = {table_name}.{brand_column_name}
        )
    ''')

# Function to populate BrandKeys table with unique brand names
def populate_brand_keys_table(cur, brand_names):
    for brand_name in brand_names:
        cur.execute('''
            INSERT OR IGNORE INTO BrandKeys (brand) VALUES (?)
        ''', (brand_name,))

# Function to update a table to replace brand names with integer keys
def update_table_with_brand_keys(cur, table_name, brand_column_name):
    cur.execute(f'SELECT * FROM {table_name}')
    table_data = cur.fetchall()
    for row in table_data:
        brand_name = row[table_data[0].index(brand_column_name)]
        cur.execute('''
            SELECT id FROM BrandKeys WHERE brand = ?
        ''', (brand_name,))
        brand_key = cur.fetchone()
        if brand_key:
            cur.execute(f'''
                UPDATE {table_name}
                SET {brand_column_name}_id = ?
                WHERE {brand_column_name} = ?
            ''', (brand_key[0], brand_name))

# Main function
def main():
    # Connect to SQLite database
    conn, cur = connect_to_database('your_database.db')

    # Handle currency column
    create_currency_keys_table(cur)
    currency_names = ['USD', 'EUR', 'GBP']  # Example list of unique currency names
    populate_currency_keys_table(cur, currency_names)
    tables_with_currency_column = ['myfoundation', 'mymascara', 'myblush', 'mybronzer']  # Replace with your table names
    for table_name in tables_with_currency_column:
        update_table_with_currency_keys(cur, table_name, 'currency')

    # Handle brand column
    create_brand_keys_table(cur)
    brand_names = ['nyx', 'glossier', 'marienatie', 'rejuva minerals', 'w3llpeople', 'deciem', 'colourpop', 'iman', 'dior', 'c’est moi', 'green people', 'lotus cosmetics usa', 'clinique', 'stila', 'marcelle', 'smashbox', 'benefit']
    populate_brand_keys_table(cur, brand_names)
    tables_with_brand_column = ['myfoundation', 'mymascara', 'myblush', 'mybronzer']  # Replace with your table names
    for table_name in tables_with_brand_column:
        update_table_with_brand_keys(cur, table_name, 'brand')

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()

