import csv
import MySQLdb

# installing MySQL: https://dev.mysql.com/doc/refman/8.0/en/osx-installation-pkg.html
# how to start, watch: https://www.youtube.com/watch?v=3vsC05rxZ8c
# or read this (absolutely helpful) guide: https://www.datacamp.com/community/tutorials/mysql-python

# this is mainly created to get a database of all the songs in my Favorites playlist
# if you wish to change the topic to 'FILM', 'SPORTS', or 'POLITICS'

# 1/ initially, set up the MySQL connection and craft a cursor
mydb = MySQLdb.connect(host='localhost', user='root', passwd='yourPasswordHere')
cursor = mydb.cursor()

# 2/ create a database:
cursor.execute("CREATE DATABASE mydb")
mydb.commit()

# 3/ after database is created, comment out steps 1/ and 2/ and uncomment step 3/
# mydb = MySQLdb.connect(host='localhost', user='root', passwd='', database="mydb")
# cursor = mydb.cursor()

# from here on out, whenever you call `cursor.execute()`, call `mydb.commit()` right afterwards

# 4/ create a table -- three options available to you
# the table's hardcoded right now so if the columns here are changed then other
def initialise_main_music_table(table_name):
    cursor.execute("CREATE TABLE " + table_name
                    + " (songID INTEGER PRIMARY KEY AUTO_INCREMENT, \
                    songTitle VARCHAR(150) NOT NULL, \
                    artist VARCHAR(100) NOT NULL, \
                    genre VARCHAR(100) NOT NULL, \
                    videoLink VARCHAR(100) NOT NULL, \
                    viewCount BIGINT NOT NULL, \
                    likeToDislikeRatio decimal(5, 4) NOT NULL)")
    mydb.commit()

# the main music table helps extract info to create sub tables for a specific music category
def initialise_custom_music_table(table_name, main_music_table_name):
    cursor.execute("CREATE TABLE " + table_name
                    + " (categorySongID INTEGER PRIMARY KEY AUTO_INCREMENT, \
                    mainSongID INTEGER NOT NULL DEFAULT 1, \
                    FOREIGN KEY(mainSongID) REFERENCES " + main_music_table_name + "(songID), \
                    songTitle VARCHAR(150) NOT NULL, \
                    artist VARCHAR(100) NOT NULL, \
                    genre VARCHAR(100) NOT NULL, \
                    videoLink VARCHAR(100) NOT NULL, \
                    viewCount BIGINT NOT NULL, \
                    likeToDislikeRatio decimal(5, 4) NOT NULL)")
    mydb.commit()

# def create_custom_table(table_name):
#     cursor.execute("CREATE TABLE " + table_name
#                     + " (tableID INTEGER PRIMARY KEY AUTO_INCREMENT, \
#                     videoTitle VARCHAR(150) NOT NULL, \
#                     author VARCHAR(100) NOT NULL, \
#                     category VARCHAR(100) NOT NULL, \
#                     videoLink VARCHAR(100) NOT NULL, \
#                     viewCount BIGINT NOT NULL, \
#                     likeToDislikeRatio decimal(5, 4) NOT NULL)")
#     mydb.commit()

# 5/ from a list of wanted fields, the function searches for the index corresponding to each field on the list
# and stores the index inside a dict (easy to look up and flexible if the order of the columns in the csv file is changed)
def get_indices_of_csv_table_items(csv_file_name, wanted_items):
    indices = {}
    with open(csv_file_name) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        csv_headings = next(csv_data)
        for idx, heading in enumerate(csv_headings):
            if heading in wanted_items:
                indices[heading] = idx
    csv_file.close()
    return indices

wanted_items = ['song_name', 'artist', 'topics', 'video_link', 'view_count', 'like_to_dislike_ratio']

# 6/ fill up our main table with the relevant data
def populate_main_music_table_from_csv(csv_file_name, table_name):
    indices = get_indices_of_csv_table_items(csv_file_name, wanted_items)
    with open(csv_file_name) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        csv_headings = next(csv_data)
        for idx, row in enumerate(csv_data):
            song_name = row[indices['song_name']]
            artist = row[indices['artist']]
            if ' - Topic' in artist:
                artist = artist[:artist.index(' - Topic')]
            genre = row[indices['topics']][1:-1]
            video_link = row[indices['video_link']]
            view_count = int(row[indices['view_count']])
            ratio = 0
            if row[indices['like_to_dislike_ratio']]:
                ratio = float(row[indices['like_to_dislike_ratio']][:-1]) / 100

            if 'MUSIC' in genre:
                cursor.execute(f"INSERT INTO {table_name} (songTitle, artist, genre, videoLink, viewCount, likeToDislikeRatio)\
                                VALUES(%s, %s, %s, %s, %s, %s)", (song_name, artist, genre, video_link, view_count, ratio))
    mydb.commit() # remember to commit after populating the table
    csv_file.close()

# 7/ fill up our custom table using data from the main music table
def populate_custom_music_table(your_new_table_name, main_music_table_name, column, chosen_value):
    cursor.execute(f"INSERT INTO {your_new_table_name} (mainSongID, songTitle, artist, genre, videoLink, viewCount, likeToDislikeRatio)\
                    SELECT songID, songTitle, artist, genre, videoLink, viewCount, likeToDislikeRatio \
                    FROM {main_music_table_name} WHERE {column} LIKE '%{chosen_value}%'")
    mydb.commit()

# -------------------------------------------------------------------
# -------------------SUPPLEMENTARY FUNCTIONS START-------------------
# -------------------------------------------------------------------

# add a field after table is created (new field placed after a specific column of a table)
def add_new_column(table_name, new_column_name, data_type, pivot_column):
    cursor.execute(f"ALTER TABLE {table_name} ADD {new_column_name} {data_type} NOT NULL AFTER {pivot_column}")
    mydb.commit()

# change data type for any given field
def modify_data_type(table_name, column_name, new_data_type):
    cursor.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {new_data_type}")
    mydb.commit()

# delete all the data from a specified table
def delete_data_from_table(table_name):
    cursor.execute(f"DELETE FROM {table_name}")
    mydb.commit()

def delete_selected_record_from_table(table_name, record):
    cursor.execute(f"DELETE FROM {table_name} WHERE address = {record}")
    mydb.commit()

# make a table disappear from existence :)
def drop_table(table_name):
    cursor.execute(f"DROP TABLE {table_name}")
    mydb.commit()

def print_table_plain(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    for row in result:
        print(row)

# print out all the songs in the playlist
# 'DESC' means descending order (most popular song on top) and 'ASC' is the opposite
def print_table_by_criteria(table_name, order_criteria, order):
    if order_criteria != '' and order != '':
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY {order_criteria} {order}")
        for item in cursor:
            print(item)

# show the name of all the tables present in the database
def show_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(tables)

# check if a table already exists
def check_table_exists(table_name):
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(table_name.replace('\'', '\'\'')))
    return True if cursor.fetchone()[0] == 1 else False

# optional / not required function: should you wish to look up the different video topics
# if you want to search for all topics, leave `selected_topic` as an empty string
def get_all_selected_topics(csv_file_name, selected_topic):
    res = []
    indices = get_indices_of_csv_table_items(csv_file_name, wanted_items)
    with open(csv_file_name) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        csv_headings = next(csv_data)
        for idx, row in enumerate(csv_data):
            topics = row[indices['topics']][1:-1]
            topic_list = topics.split(', ')
            for item in topic_list:
                if selected_topic in item and item not in res:
                    res.append(item)
    return res

# ------------------------------------------------------------------
# -------------------SUPPLEMENTARY FUNCTIONS ENDS-------------------
# ------------------------------------------------------------------

# 8/ Create main music table
def build_main_music_table(csv_file_name, main_music_table_name):
    initialise_main_music_table(main_music_table_name)
    populate_main_music_table_from_csv(csv_file_name, main_music_table_name)

# 9/ Build a new music table based on the genre you love
def build_your_custom_music_table(your_new_table_name, main_music_table_name, column, chosen_value):
    if check_table_exists(main_music_table_name) == False:
        build_main_music_table(main_music_table_name)

    initialise_custom_music_table(your_new_table_name, main_music_table_name)
    populate_custom_music_table(your_new_table_name, main_music_table_name, column, chosen_value)

def main(): # example; feel free to change the variable names to your choosing
    csv_file_name = 'favorite-playlist.csv' # name of csv file (use `main-extractor.py` first to create a csv file)
    your_new_table_name = 'ElectronicMusic' # name your table
    main_music_table_name = 'MainMusic' # name the main music table
    column = 'genre' # column choices: songTitle, artist, genre, videoLink, viewCount, likeToDislikeRatio
    chosen_value = 'ELECTRONIC MUSIC' # what you'd like to query, e.g. artist name or song title or genre
    # to get a list of all possible video topics or music genres, you can run the function get_all_selected_topics()
    # e.g. get_all_selected_topics('favorite-playlist.csv',

    order_criteria = 'viewCount' # e.g. viewCount or likeToDislikeRatio or artist name in alphabetical order
    ascending_order = False # change to true if you want to print the table in ascending order (i.e. lowest order at the top)
    order = 'ASC' if ascending_order == True else 'DESC'
    build_your_custom_music_table(your_new_table_name, main_music_table_name, column, chosen_value)
    print_table_by_criteria(your_new_table_name, order_criteria, order)

if __name__ == "__main__":
    main()
