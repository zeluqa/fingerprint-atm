#!/usr/bin/python
# datademo.py 
# a simple script to pull some data from MySQL

import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")

#create a cursor for the select
cur = db.cursor()

#execute an sql query
cur.execute("SELECT firstname,lastname FROM test.name")

##Iterate 
for row in cur.fetchall() :
      #data from rows
        firstname = str(row[0])
        lastname = str(row[1])

      #print 
        print "This Person's name is " + firstname + " " + lastname

# close the cursor
cur.close()

# close the connection
db.close ()
