import psycopg2

connection = psycopg2.connect('dbname=tobisupreme')

# Open a cursor to perform database operations
cursor = connection.cursor()

cursor.execute('''
  CREATE TABLE anothertable (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

cursor.execute('INSERT INTO anothertable (id, completed) VALUES (1, true);')

connection.commit()

cursor.close()
connection.close()