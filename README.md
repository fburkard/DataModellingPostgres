Do the following steps in your README.md file.
# Table of contents
## Purpose of this database
This database enables queries on song plays which are being accessed by different users.

## Launch
1. Run create_tables.py initially
2. Execute etl.py

## Explanation of the files in the repository
sql_queries.py: creates tables and insert statements for the database
test.ipynb: basic testing for the created tables and inserted data.
etl.ipynb: executes insert statements for individual tables. Attention: not all files are selected to insert data.
etl.py: selects all data from files and inserts selected data into the database. Attention: All files are selected.


## State and justify your database schema design and ETL pipeline
The database is built as a star schema. 
users, songs, artists and time when songs are played can be accessed individually.
The songplays table contains IDs which are connected to each individual table (users, songs, artists, time)


Provide DOCSTRING statement in each function implementation to describe what each function does.