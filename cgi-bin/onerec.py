#!/usr/bin/env python
'''This program will receive a fileid argument as a get string, viz. "<url>?fileid=1009".
   Then it looks up that record in the files database. It displays that record.
   Later, we want this program to handle Edit and Delete requests. '''

import sys
import os
import mycgi
import sqlite3

from MyFile import *


# Updated: Friday, July  5, 2024 17:44:11  .
form = mycgi.Form()

def parse_GET():
    w('...entered parse_GET()\n')
    q = os.environ.get('QUERY_STRING','There is no query string')
    w(f'GET string = {q}\n')
    if not q.startswith('fileid='):
        # Do some kind of error message
        w('** We errored out on the fileid int conversion.\n')
        w(f'Query String = {q}\n')
        return None
    else:
        n = q.index('=')
        fileident = q[n+1:]
        return int(fileident)
    
def next_fileid(fid: int):
#    w(f'\n..entering next_fileid on {today} at {now()}\n')
#    w(f'curr. fileid = {fid}\n\n)'
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = f'SELECT fileid FROM newfiles WHERE fileid > {fid} LIMIT 1'
    cur.execute(sql)
    t = cur.fetchone()
    con.close()
    if t is None:
        return fid
    else:
        return t[0]
  
def prev_fileid(fid: int)-> int:
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = f'SELECT MAX(fileid) FROM newfiles WHERE fileid < {fid}'
    cur.execute(sql)
    t = cur.fetchone()
    con.close()
    if t:
        rv = t[0] if isinstance(t[0],int) else int(t[0])
    else:
        rv = fid
    return rv
    
def main_menu():
    redirect='<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>'
    
    print('Content-Type: text/html\n\n')
    print(redirect)
    return 0
    
def report_py():
    redirect='<html><head><meta http-equiv="refresh" content="0;url=/cgi-bin/report.py"></head><body><p>Redirecting to menu.html...</p></body></html>'
    
    print('Content-Type: text/html\n\n')
    print(redirect)
    return 0
    
    
def htmlpage(thefile):
    w('\n...entered htmlpage()\n')
    
    myhtml = '''
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>Onerec</title>
<link rel="stylesheet" href="/css/onerec.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
</head>'''

    w('...wrote out the header of the new page.\n')
    
    myhtml += f'''
 <body>
    <header>Details of the file and options to change or delete the file from the database</header>
    <nav><a href="/menu.html">Home</a><a href="/lookup.html">Look up a file</a>
    <a href="/cgi-bin/report.py">View all files</a><a href="/cgi-bin/report.py">Edit or Delete</a></nav>
    
<h2>Record {thefile.fileid}</h2>'''
    
    w('\n...about to create the table.\n')
    
    # first, get the dates into the correct format
    if thefile.dt is None:
        dt = thefile.dt
    else:
        dt = ymd2dt(thefile.dt)
    cr = ymd2dt(thefile.cr)
    
    myhtml += f'''
<table><tr><th>Field</th><th>Value</th></tr>
  <tr><td>File id:</td><td>{thefile.fileid}</td></tr>
  <tr><td>Contents:</td><td>{thefile.sd}</td></tr>
  <tr><td>More details:</td><td>{thefile.ld}</td></tr>
  <tr><td>Location:</td><td>{locations[thefile.lo]}</td></tr>
  <tr><td>Owner:</td><td>{thefile.owner}</td></tr>
  <tr><td>Comments:</td><td>{thefile.comments}</td></tr>
  <tr><td>Created on:</td><td>{cr}</td></tr>'''

    
    if dt is not None:
        myhtml += f'<tr><td>Updated on:</td><td>{dt}</td></tr>'
    myhtml += '</table>'
    
    w('...created the table!\n')
    # get the next and previous file ids:
    nextid = next_fileid(thefile.fileid)
    w(f'{nextid = }\n')
    previd = prev_fileid(thefile.fileid)
    w(f'{previd = }\n')
    
    myhtml += f'''<p />
    <button id="prev" name="prev" onclick="location.href='/cgi-bin/onerec.py?fileid={previd}';">&lArr;Previous</button>&nbsp;<button id="next" name="next" onclick="location.href='/cgi-bin/onerec.py?fileid={nextid}';">Next&rArr;</button>
<hr /><p />
<div style="display: flex;">
<button style="margin:right:20px;" id="edit" name="edit" onclick="location.href='/cgi-bin/edit.py?fileid={thefile.fileid}';" />Edit</button>&nbsp;
<button  style="margin:right:20px;" id="del" name="del" onclick="location.href='/cgi-bin/confirmdel.py?fileid={thefile.fileid}';" />Delete</button>&nbsp;
<button  style="margin:right:20px;" name="menu" id="menu" onclick="location.href='/menu.html';">Home</button>&nbsp;
<button  style="margin:right:20px;" id="print" name="print" onclick="location.href='/cgi-bin/temppage.py';">Print</button>
</div>
<br /><br /><br />
<div class="copy">
  <div class="copy-text">
    <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
  </div>
</div></body></html>'''
    
    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0


def return_simple_error_page(e,tup):
    myhtml = f'''
<html><body style="bgcolor: black; color: lightred;">
    <h1><center>An Exception has been encountered.</center></h1>
    <h5><center>Please try again later</center></h5>
    <p>{e}</p>
    <p>{tup[0]}: {tup[1]}</p>
    <p>{tup[2]}</p>
    <hr />
</body><html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)

def main():
    w(f'Starting main() in {prog}.\n')
    button = form.getvalue('submit')
    w(f'{button = }\n')
    
    fileid = parse_GET()
    w(f'{fileid = }\n')
    if fileid:
        thisfile = makeonefile(fileid)
        htmlpage(thisfile)
    else:
        return 99


if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now()}.\n\n')
    rv = main()
    sys.exit(rv)
