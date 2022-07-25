import psycopg2

# define database to connect to
dbtobisupreme = 'dbname=tobisupreme'

# connect to db
conn = psycopg2.connect(dbtobisupreme)

# open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos_track table
cur.execute("DROP TABLE IF EXISTS todos_track;")

# recreate the todos_track table
cur.execute('''
  CREATE TABLE todos_track (
    id serial PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

# commit the changes to the db
conn.commit()

cur.close()
conn.close()