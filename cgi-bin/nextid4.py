#!/usr/bin/env python
''' This program returns the highest file id from the newtables table
    of the dkfiles database'''

import sys
import sqlite3
from MyFile import *


con = sqlite3.connect(db)
cur = con.cursor()
sql = 'SELECT MAX(fileid) FROM newfiles WHERE fileid < 9000'
cur.execute(sql)
row = cur.fetchone()
nextid = row[0] + 1
if nextid >= 9000:
    nextid= 1001
    
print('Content-type: text/html;charset=utf-8\n\n')
print(nextid)



if __name__ == '__main__':
    rv = main()

