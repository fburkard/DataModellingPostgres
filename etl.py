import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    this function accesses the available song files and extracts the columns which are important for the songs table and artist table
    for each file the available data is inserted into the time and user table
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

import io

#helpful was: https://naysan.ca/2020/06/21/pandas-to-postgresql-using-psycopg2-copy_from/
# helpful was also: https://knowledge.udacity.com/questions/426431
def copy_from_stringio(cur, filepath):
    """
    this function accesses the available log files and extracts the columns which are important for the time table
    for each file the available data is inserted into the time table using copy_from and then inserted into the correct time_table with upsert commands
    """
    time_table_create_tmp = ("CREATE TEMP Table If not Exists tmp_time(start_time TIMESTAMP, hour int, day int, week int, month int, year int, weekday varchar) ON COMMIT DROP;")
    cur.execute(time_table_create_tmp)
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    filterdata = ["NextSong"]
    df = df[df.page.isin(filterdata)]
    t = pd.to_datetime(df['ts']) 
    time_data = [t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    test = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(test)
    buffer = io.StringIO()
    time_df.to_csv(buffer, index= False, header=False)
    buffer.seek(0)
    #print(buffer.read())
    cur.copy_from(buffer, 'tmp_time', sep=",")
    cur.execute(time_table_insert_tmp) 

def process_log_file(cur, filepath):
    """
    this function accesses the available log files and extracts the columns which are important for the songplay table and user table
    for each file the available data is inserted into the user and songplay table
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    filterdata = ["NextSong"]
    df = df[df.page.isin(filterdata)]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts']) 
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    test = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(test)

    # uncomment this loop for removing "copy_from"
    # this loop was initially used for inserting data into time_table. It can be used when improved version of copy_from is not used
    #for i, row in time_df.iterrows():
    #    cur.execute(time_table_insert, list(row))

     
    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


 

def process_data(cur, conn, filepath, func):
    """ 
    this function iterates over all existing files from the songs and log directory and commits the data to the database
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    this function connects to the local database and executes the functions to access data from the files and insert it into the database
    connection is closed to the database
    """
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres password=udacitytest")
    cur = conn.cursor()
    process_data(cur, conn, filepath='data/log_data', func=copy_from_stringio)
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    conn.close()


if __name__ == "__main__":
    main()