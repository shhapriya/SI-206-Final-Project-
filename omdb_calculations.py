# OMDB CALCULATIONS

import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('complete.db')
cursor = conn.cursor()

# CALCULATIONS CODE

def calculate_average_rating_imdb(cur):
    cur.execute("""
        SELECT AVG(COALESCE(imdb, 0)) FROM Movie_Ratings
                """)
    average_imdb_ratings = cur.fetchone()[0]
    return average_imdb_ratings

def calculate_average_rating_rotten_tomatoes(cur):
    cur.execute("""
        SELECT AVG(COALESCE(rotten_tomatoes, 0)) FROM Movie_Ratings
                """)
    average_rotten_tom_ratings = cur.fetchone()[0]
    return average_rotten_tom_ratings

def calculate_average_rating_metacritic(cur):
    cur.execute("""
        SELECT AVG(COALESCE(metacritic, 0)) FROM Movie_Ratings
    """)
    average_metacritic_ratings = cur.fetchone()[0]
    return average_metacritic_ratings

def calculate_percentage_rating_above_two_imdb(cur):
    cur.execute("""
        SELECT imdb FROM Movie_Ratings WHERE imdb > 2.0 AND imdb IS NOT NULL
    """)
    ratings_above_two = cur.fetchall()
    count_ratings_above_two_imdb = len(ratings_above_two)
    count_ratings_above_two_imdb = int(count_ratings_above_two_imdb)
    #the_percentage = count_ratings_above_two / the_total
    return count_ratings_above_two_imdb

def calculate_percentage_rating_above_two_metacritic(cur):
    cur.execute("""
        SELECT metacritic FROM Movie_Ratings WHERE metacritic > 2.0 AND metacritic IS NOT NULL
    """)
    ratings_above_two = cur.fetchall()
    count_ratings_above_two_metacritic = len(ratings_above_two)
    count_ratings_above_two_metacritic = int(count_ratings_above_two_metacritic)
    #the_percentage = count_ratings_above_two / the_total #maybe change the total
    return count_ratings_above_two_metacritic


def write_calculated_data(average_imdb_ratings, average_rotten_tom_ratings, average_metacritic_ratings, count_ratings_above_two_imdb, count_ratings_above_two_metacritic):
    with open('calculated_data_movies.txt', 'w') as f:
        f.write("Average Rating for IMDB: {:.2f}\n".format(average_imdb_ratings))
        f.write("Average Rating for Rotten Tomatoes: {:.2f}\n".format(average_rotten_tom_ratings))
        f.write("Average Rating for Metacritic: {:.2f}\n".format(average_metacritic_ratings))

        f.write(" Percent of Ratings Above Two for IMDB: {:.2f}\n".format(count_ratings_above_two_imdb))
        f.write(" Percent of Ratings Above Two for Metacritic: {:.2f}\n".format(count_ratings_above_two_metacritic))


# STARTING VISUALIZATION CODE

def fetch_movie_ratings(cur):
    cur.execute("SELECT imdb, rotten_tomatoes FROM Movie_Ratings WHERE imdb IS NOT NULL AND rotten_tomatoes IS NOT NULL")       
    return cur.fetchall()

def calculate_regression_line(x, y):
    coef = np.polyfit(x, y, 1)
    return coef

def main (): 
 conn = sqlite3.connect('complete.db')
 cursor = conn.cursor()
 
 average_rating_imdb = calculate_average_rating_imdb(cursor)
 average_rating_rotten_tomatoes = calculate_average_rating_rotten_tomatoes(cursor)
 average_rating_rotten_metacritic = calculate_average_rating_metacritic(cursor)

 percentage_rating_above_two_imdb = calculate_percentage_rating_above_two_imdb(cursor)
 percentage_rating_above_two_metacritic = calculate_percentage_rating_above_two_metacritic(cursor)

 write_calculated_data(average_rating_imdb, average_rating_rotten_tomatoes, average_rating_rotten_metacritic, percentage_rating_above_two_imdb, percentage_rating_above_two_metacritic)


 ratings = fetch_movie_ratings(cursor)
 imdb_ratings = [rating[0] for rating in ratings]
 rotten_tomatoes_ratings = [rating[1] for rating in ratings]
 plt.figure(figsize=(8, 6))
 plt.scatter(imdb_ratings, rotten_tomatoes_ratings, c='hotpink', alpha=0.7)
 coef = calculate_regression_line(imdb_ratings, rotten_tomatoes_ratings)
 plt.plot(np.array(imdb_ratings), np.polyval(coef, np.array(imdb_ratings)), color='mediumpurple')
 plt.xlabel('IMDB Ratings')
 plt.ylabel('Rotten Tomatoes Ratings')
 plt.title('Scatter Plot of IMDB vs Rotten Tomatoes Ratings with Regression Line')
 plt.grid(True)
 plt.tight_layout()
 plt.show()

 conn.close()

 #r value and line on scatterplot??


if __name__ == "__main__":
        main()


# write every calcualtion to a txt file (the same txt file)
# make sure the calcs dont include NULL values