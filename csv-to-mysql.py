import csv
import MySQLdb

# installing MySQL: https://dev.mysql.com/doc/refman/8.0/en/osx-installation-pkg.html
# how to start, watch: https://www.youtube.com/watch?v=3vsC05rxZ8c

# 1/ initially, set up the MySQL connection and craft a cursor
# mydb = MySQLdb.connect(host='localhost', user='root', passwd='yourPasswordHere')
# cursor = mydb.cursor()

# 2/ create a database:
# cursor.execute("CREATE DATABASE mydb")
# mydb.commit

# 3/ after database is created, comment steps 1/ and 2/
mydb = MySQLdb.connect(host='localhost', user='root', passwd='', database="mydb")
cursor = mydb.cursor()

# from here on out, whenever you call `cursor.execute()`, call `mydb.commit()` right afterwards

# 4/ create a table
# the table's hardcoded right now so if the columns here are changed then other
def create_table(table_name):
    cursor.execute("CREATE TABLE " + table_name
                    + " (songID INTEGER PRIMARY KEY AUTO_INCREMENT, \
                    songTitle VARCHAR(100) NOT NULL, \
                    artist VARCHAR(100) NOT NULL, \
                    genre VARCHAR(100) NOT NULL, \
                    videoLink VARCHAR(100) NOT NULL, \
                    viewCount BIGINT NOT NULL, \
                    likeToDislikeRatio decimal(5, 4) NOT NULL)")
    mydb.commit()

# just an example; don't uncomment;
# cursor.execute(
#             'INSERT INTO Music (songTitle, artist, genre, videoLink, likeToDislikeRatio) \
#             VALUES("%s", "%s", "%s", "%s", "%s")', \
#             ('Eat Them Apples', "Suzi Wu-Topic", 'INDEPENDENT MUSIC', "https://www.youtube.com/watch?v=Bs7lVqYBqys", 0.9710))

# 4.1/ if you want to add a field after table is created (new field placed after a specific column of a table)
def add_new_column(table_name, new_column_name, data_type, pivot_column):
    cursor.execute("ALTER TABLE " + table_name + " ADD " + new_column_name + " " + data_type + " NOT NULL AFTER " + pivot_column)
    mydb.commit()

# 4.2/ if you want to change data type for any given field
def modify_data_type(table_name, column_name, new_data_type):
    cursor.execute("ALTER TABLE " + table_name + " MODIFY COLUMN " + column_name + " " + new_data_type)
    mydb.commit()

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
    return indices

# optional / not required function: should you wish to look up the different video topics
# if you want to search for all topics, leave `selected_topic` as an empty string
def get_all_selected_topics(csv_file_name, selected_topic):
    res = []
    wanted_items = ['song_name', 'artist', 'topics', 'video_link', 'view_count', 'like_to_dislike_ratio']
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

# 6/ fill up our table with the relevant data
def populate_table_from_csv(csv_file_name, table_name, selected_topic):
    wanted_items = ['song_name', 'artist', 'topics', 'video_link', 'view_count', 'like_to_dislike_ratio']
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

            if selected_topic in genre:
                cursor.execute('INSERT INTO ' + table_name + \
                                ' (songTitle, artist, genre, videoLink, viewCount, likeToDislikeRatio) \
                                VALUES("%s", "%s", "%s", "%s", "%s", "%s")', \
                                (song_name, artist, genre, video_link, view_count, ratio))

# delete the entire table
def delete_whole_table(table_name):
    cursor.execute('DELETE FROM ' + table_name)
    mydb.commit()

def delete_selected_record_from_table(table_name, record):
    cursor.execute('DELETE FROM ' + table_name + ' WHERE address = ' + record)
    mydb.commit()


# print out all the songs in the playlist (most popular on top)
def print_items(table_name):
    cursor.execute("SELECT * FROM " + table_name + " ORDER BY viewCount DESC")
    for item in cursor:
        print(item)

def main():
    table_name = 'IndieMusic'
    selected_topic = 'INDEPENDENT MUSIC'
    csv_file_name = 'favorite-playlist.csv'
    create_table(table_name)
    populate_table_from_csv(csv_file_name, table_name, selected_topic)
    print_items(table_name)

main()
# print_items('Music')
