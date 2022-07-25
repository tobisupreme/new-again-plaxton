import psycopg2

# define database to connect to
dbname = 'dbname=tobisupreme'

# initiate connection with named db
conn = psycopg2.connect(dbname)

# open cursor for session transactions
cur = conn.cursor()

# add rows to todos table
cur.execute('''
  INSERT INTO todos (id, description) VALUES (1, 'Text Prathi');
  INSERT INTO todos (id, description) VALUES (2, 'Paint Flamingos');
''')

# commit changes
conn.commit()

# sign off and close connection
cur.close()
conn.close()
