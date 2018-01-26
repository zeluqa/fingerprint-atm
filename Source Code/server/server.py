#!/usr/bin/python
# server.py 
# Module berisi fungsi-fungsi yang berhubungan dengan server diantaranya
# melakukan fetch data, update data

import MySQLdb

def connect():
	# Connect to the database
	db = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="fingershield")
	return db

def cursor(db):
	# Create a cursor to traverse the database
	cur = db.cursor()
	return cur

def close(db, cur):
	# Close the cursor
	cur.close()

	# Close the connection
	db.close()
	return	

def fetch(cur, kode):
	# Execute an sql query
	cur.execute("""SELECT * FROM nasabah where kode = %s""", (kode,))
	return cur.fetchone()

def update(db, cur, kode, saldo):
	# Execute an sql query
	cur.execute("""UPDATE nasabah SET saldo = %s WHERE kode = %s""", (saldo, kode))
	db.commit()
	return
	
'''
USAGE EXAMPLE

db = connect()
cur = cursor(db)

print type(fetch(cur, 2))
update(db, cur, 2, 430000000)
print fetch(cur, 2)
update(db, cur, 2, 450000000)
print fetch(cur, 2)
close(db, cur)
'''