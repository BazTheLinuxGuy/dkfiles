#!/usr/bin/env python
'''This program will receive a fileid argument as a get string, viz. "<url>?fileid=1009".
   Then it looks up that record in the files database. It displays that record.
   Later, we want this program to handle Edit and Delete requests. '''

import sys
import os
import mycgi
import sqlite3

from MyFile import *

def parse_GET():
    q = os.environ.get('QUERY_STRING','There is no query string')
    if q.startswith('fileid='):
        n = q.index('=')
        fileident = q[n+1:]
        return int(fileident)
    else:
        # Do some kind of error message
        w('** We errored out on the fileid int conversion.\n')
        sys.exit(99)

def return_html_page(record: tuple):
    w('In return_html_page, loading up all the values...\n')
    rec = onefile._make(record)
    w('\n...finished loading the values.\n')
    w('\n...about to start creating the html page...\n')
    myhtml = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" />
<title>Really delete?</title>
<link rel="stylesheet" href="/css/entry.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Sriracha&display=swap');
  body { margin: 10px; box-sizing: border-box; background-color: #e1e1e1; color: #004066; }
  header { display: flex; background-color: #004066; color: #e1f1f1; font-size:10pt;
           font-family: Georgia,Verdana,sans-serif; }
  table,th,td { border: 2px solid black; }
  th,td { padding-left: 15px; padding-right: 15px; }
  p { font-size: 16pt; margin: 12px; }
  nav { background-color: #ffffff; display: flex; }
  a { text-align: left; padding-right: 25px; color: navy; }
  .copy {	position: relative; justify-content: left; align-items: bottom;	padding: 40px 0px; }
  .copy-text p { position: absolute; font-size: 7pt; font-weight: bold; color: black; margin: 10px 0; bottom: auto; }
</style></head>'''

    w('...wrote out the header of the new page.\n')
    w('...this is a test sentence.\n')
    
#    myhtml += f'''
    topofpage = f'''<body><nav><a href="/menu.html">Home (Menu)</a><a href="/lookup.html">Look up</a>
<a href="/report.html">All files</a><a href="/change.html">Edit or Delete</a></nav>
<header>This page asks you to confirm deletion from the sql database</header>
<h2>Record {rec.fileid}</h2>'''
    w(f'\n{topofpage = }\n')
    w('\n...about to create the table.\n')
    myhtml += topofpage
    # change the display dates from "2024-06-29" to "Jun 29, 2024 Sat"

    cr = ymd2dt(rec.cr)
    
    myhtml += f'''
<table><tr><th>Field</th><th>Value</th></tr>
       <tr><td>File id:</td><td>{rec.fileid}</td></tr>
       <tr><td>Contents:</td><td>{rec.sd}</td></tr>
       <tr><td>More details:</td><td>{rec.ld}</td></tr>
       <tr><td>Location:</td><td>{locations[rec.lo]}</td></tr>
       <tr><td>Owner:</td><td>{rec.owner}</td></tr>
       <tr><td>Comments:</td><td>{rec.comments}</td></tr>
       <tr><td>Created on:</td><td>{cr}</td></tr>
       <tr><td>Modified:</td><td>{today}</td></tr>
</table>'''
    
    w('...created the table!\n')
    w('...about to create the form\n')
    
    pageform = f'''<hr /><p style="color:black;font-family: "Georgia","Sriracha",cursive,sans-serif">Are you sure you want to delete this record?</p>
<form id="pageform" name="pageform" method="post" action="deleterec.py">
<input type="submit" id="submit" name="submit" value="Delete" />&nbsp;<input type="submit" id="submit" name="submit" value="Do Not Delete" />
<br /><input type="hidden" id="fileid" name="fileid" value={rec.fileid} /></form>'''
    
    w('Wrote out the form.\n')
    w(f'\n{pageform = }\n')
    myhtml += pageform
    w(f'{pageform = }')
    w('\nGoing to finish the rest of the page:\n')
    
    restofpage = '''<hr /><br /><button name="back" id="back" onclick="history.go(-1);">Go Back</button>&nbsp;
  <button name="menu" id="menu" onclick="location.href='/menu.html';">Home (Menu)</button>
  <br /><br /><br />
<div class="copy">
  <div class="copy-text">
    <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
  </div>
</div>
</body></html>'''
    
    w(f'{restofpage = }\n')
    w('\n..going to add restofpage to newhtml\n')
    myhtml += restofpage
    
    print('Content-type: text/html\n\n')
    print(myhtml)
    
#    w(f'\n{newhtml = }\n')
#    w(f'...added.\nPut together entire page. Closing {df} now.\n\n\n\n')
#    w(f'End of debugging for {prog}, {today} at {now()}\n')
#    w('*' * 76)
#    w('\n\n')
#    myfile.close()
    
    print('Content-type: text/html\n\n')
    print(newhtml)
    return 0
     
def onerec(fileid: int) -> tuple:
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        sql = f"SELECT * FROM newfiles WHERE fileid={fileid}"
        cur.execute(sql)
        row = cur.fetchone()
        con.close()
        return row
    except Exception as e:
        tup = sys.exc_info()
        return_simple_error_page(e)
        sys.exit(1)

        
def main():
    w(f'Starting main() in {prog} on {today} at {now()}.\n')
    fileid = parse_GET()
    w(f'{fileid=}\n')
    if fileid:
        row=onerec(fileid)
        return_html_page(row)
    else:
        return 99


def return_simple_error_page(e,tup):
    myhtml = f'''
<html><body style="bgcolor: black; color:lightred">
    <h1><center>An Error exception has been encountered.</center></h1>
    <h5><center>Please try again later</center></h5>
    <p>{e}</p>
    <p>{tup[0]}: {tup[1]}</p>
    <p>{tup[2]}</p>
    <hr />
</body><html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0
############################################################################################

if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now()}.\n\n')
    rv = main()
    sys.exit(rv)
