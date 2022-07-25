import psycopg2

# define database to connect to
dbname = 'dbname=tobisupreme'

# initiate connection with named db
conn = psycopg2.connect(dbname)

# open cursor for session transactions
cur = conn.cursor()

# add rows to todos_track table
cur.execute('INSERT INTO todos_track (id, completed) VALUES (%s, %s);', (1, False))

cur.execute('INSERT INTO todos_track (id, completed) VALUES (%(id)s, (%(completed)s);', {
  'id': 1,
  'completed': True
})

# commit changes
conn.commit()

# sign off and close connection
cur.close()
conn.close()
