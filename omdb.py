import requests
import json
import re
import sqlite3

# Function to read API key from a file
def read_api_key(file):
    with open(file, "r") as key_file:
        key = key_file.read().strip()
    return key

API_KEY = read_api_key("omdb_key.txt")

def get_movie_titles_from_books(num_pages, year=None):
    movie_titles = []
    for page_number in range(num_pages):
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&s=movie&type=movie&page={page_number+1}"
        if year:
            url += f"&y={year}"
        response = requests.get(url)
        print(f"API Response for page {page_number+1}: {response.text}")  # Debugging print statement
        if response.status_code == 200:
            data = json.loads(response.text)
            if data['Response'] == 'True':
                for movie in data['Search']:
                    movie_titles.append(movie['Title'])
            else:
                print(f"Error: {data['Error']}")
        else:
            print(f"Error: Unable to fetch data from OMDb API. Status code: {response.status_code}")
    return movie_titles

def clean_movie_title(title):
    # Remove additional information like the year and author name
    cleaned_title = re.sub(r'\s*Based on the Novel.*$', '', title).strip()
    return cleaned_title

# Function to convert rating values to decimals
def convert_to_decimal(value):
    try:
        match = re.search(r'(\d+(\.\d+)?)', value)
        if match:
            if float(match.group()) < 10:
                return round(float(match.group())/2, 2)
            if float(match.group()) > 10:
                return round(float(match.group())/20, 2)
        else:
            return None
    except Exception as e:
        print(f"Error converting to decimal: {e}")
        return None

# Function to fetch movie ratings
def get_movie_ratings(title):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = json.loads(response.text)
        if movie_data['Response'] == 'True':
            title = movie_data['Title']
            ratings = movie_data['Ratings']
            genres = movie_data['Genre']
            rating_decimals = {}
            for rating in ratings:
                source = rating['Source']
                value = rating['Value']
                decimal_value = convert_to_decimal(value)
                if decimal_value is not None:
                    rating_decimals[source] = decimal_value
            return title, rating_decimals, genres
        else:
            return "Error: Movie not found", None, None
    else:
        return "Error: Unable to access OMDb API", None, None

# Function to create SQLite database and tables
def create_database():
    conn = sqlite3.connect('ratings.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Genres'
                 (genre_id INTEGER PRIMARY KEY AUTOINCREMENT, genre TEXT UNIQUE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS 'Movie Ratings'
                 (title_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, imdb REAL, rotten_tomatoes REAL, metacritic REAL, genre_id INTEGER, FOREIGN KEY (genre_id) REFERENCES Genres(genre_id))''')
    conn.commit()
    conn.close()

# Function to insert ratings into SQLite database
def insert_ratings(title, ratings, genres):
    conn = sqlite3.connect('ratings.db')
    cur = conn.cursor()
    if genres is not None:
        first_genre = genres.split(', ')[0]
        cur.execute('''INSERT OR IGNORE INTO 'Genres' (genre) VALUES (?)''', (first_genre,))
        cur.execute('''SELECT genre_id FROM 'Genres' WHERE genre = ?''', (first_genre,))
        genre_row = cur.fetchone()
        if genre_row:
            genre_id = genre_row[0]
        else:
            print(f"Error: Genre ID not found for '{first_genre}'. Skipping insertion.")
            return
    if ratings is None:
        print(f"No ratings found for '{title}'. Skipping insertion.")
    else:
        cur.execute('''INSERT OR REPLACE INTO 'Movie Ratings' (title, imdb, rotten_tomatoes, metacritic, genre_id) VALUES (?, ?, ?, ?, ?)''', (title, ratings.get('Internet Movie Database', None), ratings.get('Rotten Tomatoes', None), ratings.get('Metacritic', None), genre_id))
    conn.commit()
    conn.close()

# Function to fetch movies with genres from SQLite database
def get_movies_with_genres():
    conn = sqlite3.connect('ratings.db')
    cur = conn.cursor()
    cur.execute('''SELECT m.title, m.imdb, m.rotten_tomatoes, m.metacritic, g.genre FROM 'Movie Ratings' m JOIN 'Genres' g ON m.genre_id = g.genre_id''')
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    movie_adaptations = get_movie_titles_from_books(10)  # Fetch 100 movies

    print(f"Fetched {len(movie_adaptations)} movie titles from OMDb API")

    create_database()
    conn = sqlite3.connect('ratings.db')
    cur = conn.cursor()

    cur.execute('''SELECT title FROM 'Movie Ratings' ''')
    existing_titles = set(row[0] for row in cur.fetchall())

    new_movies = []
    for title in movie_adaptations:
        cleaned_title = clean_movie_title(title)
        if cleaned_title not in existing_titles:
            new_movies.append(cleaned_title)

    for title in new_movies[:25]:  # Limit to the first 25 new movies
        ratings_output = get_movie_ratings(title)
        if ratings_output[1] is not None:  # Check if ratings are available
            insert_ratings(title, ratings_output[1], ratings_output[2])

    movies_with_genres = get_movies_with_genres()
    for movie in movies_with_genres:
        print(movie)

    conn.close()

