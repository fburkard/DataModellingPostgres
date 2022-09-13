import psycopg2

try: 
    conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=postgres user=postgres password=udacitytest")
except psycopg2.Error as e: 
    print("Error: Could not make connection to the Postgres database")
    print(e)

try: 
    cur = conn.cursor()
except psycopg2.Error as e: 
    print("Error: Could not get cursor to the Database")
    print(e)

conn.set_session(autocommit=True)


try: 
    cur.execute("SELECT * FROM users LIMIT 5;")
    
    
except psycopg2.Error as e: 
    print("Error: select *")
    print (e)

#row = cur.fetchone()
#while row:
#   print(row)
#   row = cur.fetchone()