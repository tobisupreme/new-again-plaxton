import psycopg2

connection = psycopg2.connect('dbname=tobisupreme')

cursor = connection.cursor()

# cursor.execute('''
#   CREATE TABLE anothertable (
#     id INTEGER PRIMARY KEY,
#     completed BOOLEAN NOT NULL DEFAULT False
#   );
# ''')

cursor.execute('INSERT INTO anothertable (id) VALUES (2);')

connection.commit()

cursor.close()
connection.close()