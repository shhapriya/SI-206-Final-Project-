import sqlite3

conn = sqlite3.connect('complete.db')
cursor = conn.cursor()

# LAST FM CALCULATIONS & VISUALIZATIONS
def calculate_average_playcount_top_tracks(cur):
    cur.execute("""
        SELECT Avg(Playcount) FROM top_tracks
    """)
    average_playcount_top_tracks = cur.fetchone()[0]
    return average_playcount_top_tracks

def calculate_average_playcount_top_artist(cur):
    cur.execute("""
        SELECT Avg(Playcount) FROM top_artists
    """)
    average_playcount_top_artist = cur.fetchone()[0]
    return average_playcount_top_artist

def calculate_average_playcount_per_artist(cur):
    cur.execute("""
        SELECT top_artists.name, AVG(top_tracks.Playcount) AS calculate_average_playcount
        FROM top_tracks
        JOIN top_artists ON top_tracks.artistID = top_artists.id
        GROUP by top_artists.name
    """)
    artist_playcount_per_artist = cur.fetchall()
    return artist_playcount_per_artist

def write_calculated_data(average_playcount_top_tracks, average_playcount_top_artist, average_playcount_per_artist):
    with open('calculated_data.txt', 'w') as f:
        f.write("Average Playcount for Top Tracks: {:.2f}\n".format(average_playcount_top_tracks))
        f.write("Average Playcount for Top Artists: {:.2f}\n".format(average_playcount_top_artist))
        f.write("\nAverage Playcount per Artist:\n")
        for artist, avg_playcount in average_playcount_per_artist:
            f.write(f"{artist}: {avg_playcount:.2f}\n")



def plot_by_averages (db):
    avg_ratings_by_type = {row[1]: row[2] for row in rows}
    sorted_avg_ratings_by_type = dict (sorted(avg_ratings_by_type))
    plt.figure (figsize = (10, 8))
    song_type_id = list (sorted_min_ratings_by_type.keys ())
    ratings = list (sorted_avg_ratings_)

def main(): 
    conn = sqlite3.connect('complete.db')
    cursor = conn.cursor()

    average_playcount_top_tracks = calculate_average_playcount_top_tracks(cursor)
    average_playcount_top_artist = calculate_average_playcount_top_artist(cursor)
    average_playcount_per_artist = calculate_average_playcount_per_artist(cursor)

    write_calculated_data(average_playcount_top_tracks, average_playcount_top_artist, average_playcount_per_artist)

    conn.close()

if __name__ == "__main__":
    main()









# access full database 

#averages, 
#total streams across spotify and last fm 
# percentages 

#join on something that shares an integer key (calculate how many songs top artist has) (do percentages)
