# DROP TABLES

songplay_table_drop = "Drop Table If Exists songplays"
user_table_drop = "Drop Table If Exists users"
song_table_drop = "Drop Table If Exists songs"
artist_table_drop = "Drop Table If Exists artists"
time_table_drop = "Drop Table If Exists time"
time_table_temp_drop = "Drop Table If Exists tmp_time"

# CREATE TABLES

user_table_create = ("Create Table If not Exists users(user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar);")

song_table_create = ("Create Table If not Exists songs(song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar, year int, duration float NOT NULL);")

artist_table_create = ("Create Table If not Exists artists(artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude float, longitude float);")

time_table_create = ("Create Table If not Exists time(start_time TIMESTAMP PRIMARY KEY, hour int, day int, week int, month int, year int, weekday varchar);")

songplay_table_create = ("Create Table If not Exists songplays(songplay_id SERIAL PRIMARY KEY, \
    start_time timestamp NOT NULL, user_id int NOT NULL, \
    level varchar, song_id varchar, \
    artist_id varchar, \
    session_id int, location varchar, user_agent varchar);")

# this was a try to create a tmp_table along with all other tables. then I noticed that the tmp_table is deleted after conn.closes(). 
# hence one has to put it in the code where it should be executed
#time_table_create_tmp = ("CREATE TEMP Table If not Exists tmp_time(start_time TIMESTAMP, hour int, day int, week int, month int, year int, weekday varchar) ON COMMIT DROP;")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO NOTHING;
    """)

user_table_insert = ("""
    INSERT INTO users(user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
    """)

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration) \
    VALUES (%s, %s, %s, %s, %s) \
    ON CONFLICT (song_id) DO NOTHING;
    """)

artist_table_insert = ("""
    INSERT INto artists(artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
    """)

time_table_insert_tmp = ("""INSERT INTO time 
SELECT DISTINCT ON (start_time) * FROM tmp_time ON CONFLICT DO NOTHING;
DROP TABLE IF EXISTS tmp_time
""")

# this function has to be uncommented when not using "copy_from"
#time_table_insert = ("""
#    INSERT INTO time(start_time, hour, day, week, month, year, weekday)
#    VALUES (%s, %s, %s, %s, %s, %s, %s)
#    ON CONFLICT (start_time) DO NOTHING;
#    """)

# FIND SONGS

# checked this variable with udacity knowledge
song_select = ("""SELECT songs.song_id, artists.artist_id FROM ((songs INNER JOIN artists ON songs.artist_id = artists.artist_id))\
                  WHERE songs.title= (%s) AND artists.name= (%s) AND songs.duration= (%s) \
""")


#song_select = (
#               """)
#
#"""SELECT s.song_id AS song_id, a.artist_id AS artist_id \
#FROM (songs s INNER JOIN artists a ON s.artist_id = a.artist_id) \
#WHERE s.title = %s AND a.name = %s AND s.duration = %s \
#
##("""
#    SELECT songs.song_id, artists.artist_id FROM ((songs JOIN \
#    artists ON songs.artist_id = artists.artist_id))
#    WHERE
#    songs.title=%s
#    AND arists.name=%s
#    AND songs.duration=%s;
#    """)
#
#song_select = (""" select s.song_id, a.artist_id from songs s join artists a on a.artist_id = s.artist_id where a.name = %s and s.title = %s and s.duration = %s;
#
#""")

#SELECT song_id, title, artist_id, duration FROM songs
#JOIN artists ON \
#songs.artist_id = artists.artist_id;

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop, time_table_temp_drop]
song_select_queries = [song_select]