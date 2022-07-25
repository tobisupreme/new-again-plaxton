import psycopg2

# define database to connect to
dbname = 'dbname=tobisupreme'

# initiate connection with named db
conn = psycopg2.connect(dbname)

# open cursor for session transactions
cur = conn.cursor()

# add rows to todos_track table
# cur.execute('INSERT INTO todos_track (id, completed) VALUES (%s, %s);', (1, False))

# query2 = 'INSERT INTO todos_track (id, completed) VALUES (%(id)s, %(completed)s);'
# data2 = {
#   'id': 2,
#   'completed': True
# }
# cur.execute(query2, data2)

# query3 = 'INSERT INTO todos_track (id, completed) VALUES (%(id)s, %(completed)s);'
# data3 = {
#   'id': 3,
#   'completed': False
# }
# cur.execute(query3, data3)

# fetch results
cur.execute('SELECT * FROM todos_track;')

result1 = cur.fetchone()
print('fetchone', result1)

cur.execute('SELECT * FROM todos_track;')
result2 = cur.fetchone()
print('fetchone', result2)

result3 = cur.fetchall()
print('fetchall', result3)

# commit changes
conn.commit()

# sign off and close connection
cur.close()
conn.close()
