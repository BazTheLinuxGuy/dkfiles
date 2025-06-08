#!/usr/bin/env python

import sys
import os
import sqlite3
import mycgi
import random
from collections import namedtuple 
from MyFile import *

DEBUG = 0
sr = random.SystemRandom()
form = mycgi.Form()

def fetch_records(page_number, records_per_page):
    w('\n...in fetch_records.\n')
    w(f'{page_number=}, {records_per_page=}\n')
    dt = thedate()
    con = sqlite3.connect(db)
    cur = con.cursor()
    # Calculate the offset based on the page number and records per page
    offset = (page_number - 1) * records_per_page
    # Execute the query with LIMIT and OFFSET
    sql = f'SELECT * FROM newfiles ORDER BY fileid LIMIT {records_per_page} OFFSET {offset}'
    w(f'The sql statement in fetch_records is:\n{sql}\n')
    cur.execute(sql)
    # Fetch the results
    records = cur.fetchall()
    w(f'..after fetchall there are {len(records)} records.\n')
    # Close the connection
    con.close()
    return records

def return_html(page: int, records: list):
    '''This function lays out the page generated when the user chooses "Report" '''

    w('...entered return_html()...\n')
#    dkfiles=[]
    w('\n\nin return_html()...\n')
    htmlpage = '''
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>dkfiles Report</title>
<link rel="stylesheet" href="/css/dkfiles.css" />
<style>
header { display: flex; background-color: #004066; color: #e1e1e1; font-size:10pt;
font-family: "Georgia","Sriracha",cursive,sans-serif; align-items: left; padding: 0 5px; }

body {
  background-color: lightblue;
  color: #004066;
  margin-left: 50px;
}
    
nav {
	display: flex;
	background-color: #e1f1f1;
	color: #004066;
	font-family: "Verdana","Georgia",sans-serif;
	font-size: 12pt; 
}								
a {
	color: #004066;
	background-color: #e1f1f1;
	padding-right: 20px;
	font-size: 12pt;
}

nav.nav {
	display: flex;
	background-color: #e1f1f1;
	color: #004066;
	font-family: "Verdana","Georgia",sans-serif;
	font-size: 12pt; 
}								

a.nav {
	color: #004066;
	background-color: #e1f1f1;
	padding-right: 20px;
	font-size: 12pt;
}
    
table.main { width: 70% }
td.main { padding: 0; color: pink; background-color: maroon; }
.copy {
  position: absolute;
  justify-content: bottom;
  align-items: bottom;
  padding: 50px 0 0 0;
}
.copy-text p {
  position: relative;
  font-size: 7pt;
  font-weight: bold;
  color: black;
  margin: 10 0px;
  bottom: auto;
}
    
</style></head><body>
<header>Report for dkfiles: files and descriptions.</header>
<nav><a href="/menu.html">Home</a><a href="/lookup.html">Lookup</a><a href="/change.html">Edit or Delete</a><a href="/thankyou.html">Quit Entirely</a></nav>
<br /><hr />
    <div class="main" width="80%" style="width: 80%">
    <table class="main">'''
  
    # w(f'we\'re creating an html page, so far it\'s {len(htmlpage)} characters.\n')
    
    htmlpage += f'''
    <thead class="main"><tr class="main"><th class="main" colspan="4" style="text-align: left;">Page: {page}</th></tr>
    <tr class="main"><th class="main">File id</th><th class="main">Contents</th>
        <th class="main">Location</th><th class="main">More Details</th></tr>
    <tr><th colspan="4" style="background-color: darkblue;"</th></tr>
    </thead>'''

    w('\nOK, going to enumerate the records now.\n')

    # w('...is there a problem here?\n')
    
    for i,rec in enumerate(records):
        afile = onefile._make(rec)
        #        dkfiles.append(afile)  # Why?
#        w('...enumerating the records:\n')
        fid = afile.fileid
#        w(f'...{fid = }\n')
        sd = afile.sd
#        w(f'...{sd = }\n')
        ld = afile.ld
#        w(f'...{ld = }\n')
        lo = afile.lo
#        w(f'...{lo = }\n')
        dt = afile.dt
#        w(f'...{dt = }\n')
        owner = afile.owner
#        w(f'...{owner = }\n')
        comments = afile.comments
#        w(f'...{comments = }\n')
        cr = afile.cr
#        w(f'...{cr=}\n')
        htmlpage += f'''
        <tr><td ><b>{fid}</b></td><td>{sd}</td><td >{locations[lo]}</td><td><center><button onclick="location.href='onerec.py?fileid={fid}';">GO</button></center></td></tr>
        <tr><td style="background-color: darkblue;" colspan="4"</td></tr>'''
        
    # w(f'Enumeration {i}: page has {len(htmlpage)} characters so far.\n')
        
    htmlpage += '''</table><hr /><br /><br />
    <div class="form1">
    <form class="form1" method="POST" action="/cgi-bin/report.py">
    <input type="submit" id="submit" name="submit" value="&lArr;Previous">&nbsp;
    <input type="submit" id="submit" name="submit" value="Next&rArr;"><br />
    <br />'''
    htmlpage += f'''
     <input  class="form1" type="hidden" id="pg" name="pg" value="{page+1}" />
<!--    <input  class="form1" type="hidden" id="irec" name="irec" value="{i+1}" />    -->
    </form></div>'''
    htmlpage += '''
    <hr /><br />
    <button onclick='location.href="/menu.html";'>Home (Menu)</button>
    <br />
    <div class="copy" align="bottom" >
      <div class="copy-text">
        <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
      </div>
    </body></html>'''
    
    w('We finished creating the page and now we\'re displaying all\n')
    w(f'{len(htmlpage)} characters of it.\n')
    
    myfile.close()
    
    print('Content-type: text/html\n\n')
    print(htmlpage)
    return 0

def menu():
    print('Content-Type: text/html\n\n')
    print('''<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head>''' \
          '''<body><p>Redirecting to menu.html...</p></body></html>''')

def nrecs_in_db() -> int:
    '''Returns the number of records in the database'''
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    sql = 'SELECT COUNT(*) FROM newfiles WHERE fileid < 9000'
    cur.execute(sql)
    numtuple = cur.fetchone()
    totalrecs = int(numtuple[0])
    con.close()
    w(f'{totalrecs=}\n')
    return (totalrecs)


def get5randomrecs():
    ''' Get 5 records at random '''    
    # Since we're bored and angry, we are deciding to fetch five random records,
    # rather than the first five.
    files = []
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = f'SELECT fileid FROM newfiles'
    cur.execute(sql)
    lst = cur.fetchall()
    l = [ int(row[0]) for row in lst]
    random.seed()
    random.shuffle(l)
    l = l[0:5]  # just use the first 5
    for i in l:
        sql = f'SELECT * FROM newfiles WHERE fileid = {i}'
        cur.execute(sql)
        files.append(cur.fetchone())
    return files


def handle_none(recs_per_page):
    rv = 1
    page_number = 1
    result = fetch_records(page_number, recs_per_page)
    if (len(result)):
        w(f'We got back from a trip to fetch_records, and got {len(result)} records back.\n')
        w('we\'re about to display the page...\n')
        rv = return_html(page_number, result)
    return rv


def handle_next(recs_per_page, totalrecs):
    rv = 1
    pg = form.getvalue("pg")
    w(f'Inside Next\n')
    page_number =  int(pg)
    w(f'{page_number = }\n')
    offset = (page_number - 1) * recs_per_page
    w(f'{offset=}\n') 
    if offset <= totalrecs:
        result = fetch_records(page_number, recs_per_page)
        if len(result):
            rv = return_html(page_number,result)
        else:
            page_number -= 1
            result = fetch_records(page_number, recs_per_page)
            if len(result):
                rv = return_html(page_number, result)
    else:
        w('Offset is beyond end of records, retreating back to the last page.\n')
        page_number -= 1
        result = fetch_records(page_number, recs_per_page)
        if len(result):
            rv = return_html(page_number,result)
    return rv


def handle_previous(recs_per_page, totalrecs):
    w('Inside Previous\n')
    rv = 1
    pg = form.getvalue('pg')
    page_number = int(pg)
    w(f'page number is {page_number}\n')
    if (page_number >= 3):
        page_number -= 2
    else:
        page_number = 1
    w(f'now, page number goes back to {page_number}\n')
    offset = (page_number - 1) * recs_per_page
    w(f'{offset = }, {totalrecs = }, {page_number = }\n')
    if offset <= totalrecs:
        w(f'Calling fetch_records from Previous\n')
        w(f'..as fetch_records({page_number}, {recs_per_page}\n')
        result = fetch_records(page_number, recs_per_page)
        w(f'After fetch records, len(result) = {len(result)}\n')
        if len(result) > 0:
            w(f'Calling return_html from Previous...\n')
            rv = return_html(page_number,result)
        else:
            result = fetch_records(1, recs_per_page)
            rv = return_html(page_number,result)
    return rv

            
def main():
    w('\n')
    w(f'Debugging in main() for {prog}.py at {now()}\n')
    w('\n')
    totalrecs = nrecs_in_db()
    w(f'{totalrecs=}\n')
    records_per_page = 5
    submit = form.getvalue('submit')
    if submit:
        submit = submit.lower()
        
    w(f'Submit value is {submit}\n')
    
    if submit is None:   # it is None when entering from the main menu
        w(f'Inside {prog} {submit = }\n')
        rv = handle_none(records_per_page)
        return rv
    
    elif 'next' in submit:
        w('inside Next\n')
        rv = handle_next(records_per_page, totalrecs)
        return rv
    
    elif 'previous' in submit:
        w(f'Inside Previous.\n')
        rv = handle_previous(records_per_page, totalrecs)
        return rv
    
    elif submit == 'menu':
        w(f'Inside Menu\n')
        w ('About to enter menu()\n')
        myfile.close()
        menu()
        
    else:
        w(f'Oddly, the submit button was {submit}\n.')
        myfile.close()
        menu()
    return 0
          

if __name__ == '__main__':
    w('*' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now()}.\n')
    w('This module *was* for test purposes only!\n\n')
    rv = main()
    sys.exit(rv)
