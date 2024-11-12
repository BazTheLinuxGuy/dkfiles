#!/usr/bin/env python
''' This program returns the highest file id from the newtables table
    of the dkfiles database'''

import sys
import sqlite3
from MyFile import *


def main():
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = 'SELECT MAX(fileid) FROM newfiles WHERE fileid < 9000'
    cur.execute(sql)
    row = cur.fetchone()
    nextid = row[0] + 1
    if not isinstance(nextid,int):
        print('*** nextid isn\'t an int, bailing out...')
        return -999
    if nextid is None:
        print('nextid is "None". Now we\'re really screwed.',file=sys.stderr)
        return -99
    if nextid >= 9000:
        nextid= 1001
        
    print('Content-type: text/html;charset=utf-8\n\n')
    print(f'<p>File id: {nextid}</p>')
    return nextid


if __name__ == '__main__':
    rv = main()
    sys.exit(rv)
