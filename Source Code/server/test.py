#!/usr/bin/python
# datademo.py 
# a simple script to pull some data from MySQL

import MySQLdb

db = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="fingershield")

#create a cursor for the select
cur = db.cursor()

#execute an sql query
cur.execute("SELECT * FROM nasabah")

##Iterate 
for row in cur.fetchall() :
	#data from rows
	kode = str(row[0])
	nama = str(row[1])
	kartu = str(row[2])
	saldo = str(row[3])
	valid = str(row[4])
	
	#print 
	print "kode  : " + kode
	print "nama  : " + nama
	print "kartu : " + kartu
	print "saldo : " + saldo
	print "valid : " + valid + "\n"

# close the cursor
cur.close()

# close the connection
db.close ()
