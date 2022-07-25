import psycopg2

# define database to connect to
dbtobisupreme = 'dbname=tobisupreme'

# connect to db
conn = psycopg2.connect(dbtobisupreme)

# open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS todos;")

# recreate the todos table
cur.execute('''
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
''')

# commit the changes to the db
conn.commit()

cur.close()
conn.close()