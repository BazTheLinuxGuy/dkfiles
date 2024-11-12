#!/usr/bin/env python
''' This cgi program will change or delete a dk file in the database'''

import os
import sys
import sqlite3
import mycgi
from MyFile import *

DEBUG = 1

# globals and abbreviations
debug_output = 'delrec_debug.txt'
do=debug_output

database_name='/var/data/files.db'
dbname = database_name
db = database_name

myfile = open(do,'a')
w = myfile.write

today = thedate()
now = thetime()

prog = os.path.basename(sys.argv[0])
form = mycgi.Form()


def return_error_page(e):
#    e_info: dict = { 
#        'type': type(e),    # the exception type
#        'args': e.args,     # arguments stored in .args
#        'estr': str(e),     # __str__ allows args to be printed directly
#    }
#    if not e_info['args']:
#        e_info['args'] = ''
#    tea = type(e_info['args'])

    htmlpage = '''\
<html><head>
<style>
body { text-align: left; left-margin: 100px;
       background-color: lightblue; padding: 20px 100px; }
header { display: flex; background-color: #004066;
       color: #e1e1e1; font-size:10pt; font-family: Arial;
       align-items: left; padding: 0 20px; }
h1 { color: green; text-align: left; }
h2 { color: black; text-align: left; left-margin: 100px; }
p { color: black; text-align:left; font-size: 16pt; left-margin: 100px; }
img { padding: 10px 10px; }
button { left-margin: 100px; }
table, th, td { border: 2px solid black; }
table { width: 50%; }
th { width: 30%; text-align: center; }
td { width: 30%; text-align: center; }
</style></head>
<body>
<title>Deletion Error</title>2
<header>An error has occurred while trying to delete the record</header>
<h2>You have encountered an error</h2>
<hr />
<p>Details:</p>'''
    htmlpage += f'''\
    <table>
    <tr><td align="right">Error type:</td>
       <td align="left">{type(e)}</td></tr>
    <tr><td align="right">Error args:</td>
        <td align="left:>{e.args}</td></tr>
    <tr><td align="right">The error:</td>
        <td align="left">{e}</td></tr>')
    </table>
    <p>Please contact the programmer about this issue</p>
<!-- <br /><button id="change" name="change"
            onclick="location.href=\'/change.html\';">
Edit/Delete</button> -->
    <hr />
    <button name="menu" id="menu"
            onclick="location.href=\'/menu.html\';">
Menu</button><br /></body></html>'''
    print('Content-type: text/html\n\n')
    print(htmlpage)

def get_fileid() -> int:
    q = os.environ.get('QUERY_STRING','There is no query string')
    i = q.index('=')
    i += 1
    fileidstr = q[i:]
    w(f'The file id passed in was {fileidstr}\n')
    return int(fileidstr)

def delete_row(fileid: int):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        idstr = str(fileid)
        sql = f"DELETE from newfiles WHERE fileid = {fileid}"
        w(f'The sql statementto be executed is\n>>>{sql}<<<\n')
        c = cur.execute(sql)
        con.commit()
        con.close()
    except sqlite3.OperationalError as soe:
        w(f'received sqlite.OperationalError:\n\'{soe}\'\n')
        return_error_page(soe)
    except Exception:
        w(f'received an Exception:\n\'{Exception}\'\n\n')
        tup = sys.exc_info()
        w('Unknown exception detail:\n')
        w(f'tup[0]: {tup[0]}, tup[1]: {tup[1]}\n')
        return_error_page(Exception)
#    else:
#        numtuple = c.fetchone()
#        w(f'\n{numtuple=}\n')
#        if numtuple is None:
#            numtuple = (1,)
#        totalrecs = int(numtuple[0])
#        w(f'\n{totalrecs=}\n')
#        con.close()
    w('returning 0 from delete_row\n')
    return 0

from_stack_overflow = '''\
form  { display: table;      }
p     { display: table-row;  }
label { display: table-cell; }
input { display: table-cell; }
<form>
  <p>
    <label for="a">Short label:</label>
    <input id="a" type="text">
  </p>
  <p>
    <label for="b">Very very very long label:</label>
    <input id="b" type="text">
  </p>
</form>
'''


def return_html(filenum: int):
    htmlpage= '''\
<html><head></head>
<style>
header { display: flex; background-color: #004066;
    color: #e1e1e1; font-size:10pt; font-family: Arial;
    align-items: left; padding: 0 20px; }
body {
    background-color: lightblue;
    padding: 50px; 75px; }
</style></head><body>
<title>Deleted!</title>
<header>The record you chose has been deleted</header>'''
    htmlpage += f'''\
<h2>Record {filenum} has been deleted</h2>
    <p>Click the button below to return to the menu</p>
<img src="/file-folders3.png" alt="File Folders" />
<hr /><br />
    <p><button id="menu" name="menu" onclick='location.href="/menu.html";'>Menu</button></p>
</body></html>'''
    print('Content-type: text/html\n\n')
    print(htmlpage)

    
def main():
    w('just before get fileid.\n')
    fileid = get_fileid()
    w(f'fileid is {fileid}\n')
    w('just before delete row.\n')
    rv = delete_row(fileid)
    w('Delete row went OK\n')
    w('about to create an html page...\n\n')
    myfile.close()
    return_html(fileid)

    
if __name__ == '__main__':
    w('-' * 66)
    w(f'\nin __main__, debugging {prog} on {today} {now}\n\n')
    w('\nabout to call main\n\n')
    rv = main()
