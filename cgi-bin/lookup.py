#!/usr/bin/env python
''' This cgi program responds to the form on 'lookup.html' '''

import os
import sys
import sqlite3
import mycgi
from MyFile import *

DEBUG = 0

form = mycgi.Form()

def sorry(searchterm):
    w(f'Entered "sorry({searchterm})"\n')
    
    myhtml = '''
<html><head><meta charset="utf-8"><title>Lookup Results</title>
<link rel="stylesheet" href="/css/dkfil es.css" />
<style>
body {
  text-align: left; left-margin: 75px; background-color: #e1e1e1;
  padding: 0px 20px;
}
header {
    display: flex; 
    background-color: #004066;
    color: #e1e1e1;
    font-size:10pt;
    font-family: Arial,sans-serif;
    align-items: left;
    padding-top: 0px;
    padding-left: 5px;
}
h1 { color: darkgreen; text-align: left; }
h2,h4 { color: darkgreen; text-align: left; left-margin: 75px; }
p { color: black; text-align:left; left-margin: 75px; }
img { padding: 10px 10px; }
button { left-margin: 75px; }
table, th, td { border: 2px solid black; }
table { width: 75%; }
td { padding-left: 10px; }
</style></head><body>
<nav class="nav">
<a  class="nav" href="/menu.html">Home (Menu)</a>
<a  class="nav" href="/lookup.html">Lookup another record</a>
</nav>'''
    myhtml += f'''
<header>dkfiles lookup results for '{searchterm}'</header>
<h2>Sorry!</h2>
<br /><br /><h4>We couldn't find the search term '{searchterm}'</h4><br />
<p>Please try again</p>
<button id="lookup" name="lookup" onclick="location.href='/lookup.html';">Lookup</button>
<br />
<button name="home" onclick="location.href='/menu.html';">Home</button><br />
</body></html>'''
    print('Content-type: text/html\n\n') 
    print(myhtml)
    sys.exit(1)

    
def foundit(searchterm: str, lst: list):
    w('Entered foundit()\n')
    w(f'lst is {lst}\n')

    myhtml = '''
<html><head>    
<meta charset="utf-8"><title>Lookup Results</title>
<link rel="stylesheet" href="/css/dkfiles.css" />
<style>
body {
  text-align: left; left-margin: 75px; background-color: lightblue; padding: 0px 20px; }
h1 { color: darkgreen }
h2 { color: black;}
p { color: black; font-size: 16pt; }
img { padding: 10px 10px; }
/* button { left-margin: 75px; } */
table, th, td { border: 2px solid black; }
table { width: 75%; }
td { padding-left: 10px; }
</style></head><body>'''
    myhtml += f'''    
<header>Lookup results for '{searchterm}' are in the table below</header>
<nav class="nav">
 <a class="nav" href="/menu.html">Home (Menu)</a>
 <a class="nav" href="/lookup.html">Lookup another record</a>
 <a class="nav" href="/change.html">Edit or Delete</a>
</nav>
<h2>Here's what we found for '{searchterm}'</h2>'''
    
    lenlst = len(lst)
    w(f'list length: {lenlst}, list: {lst}\n')
    if lenlst == 1:
        myhtml += f'<p>We found one match</p>'
        w('We found one match.\n')
    else:
        myhtml += f'<p>We found {lenlst} matches</p>'
        myfile.write(f'We found {lenlst} matches.\n')
        
    myhtml += '<table width="75%"><tr><th>File id</th><th>Contents</th><th>Location</th><th>More Details?</th></tr>'
    
    for i, row in enumerate(lst):   # "row" is a tuple, to be turned into a named tuple of the "onefile" type (see MyFile.py)
        e = eachfile = onefile._make(row)
        location = locations[e.lo]
        myhtml += f'''<tr><td>{e.fileid}</td><td>{e.sd}</td><td>{location}</td>
        <td><center><button onclick="location.href='/cgi-bin/onerec.py?fileid={e.fileid}';">GO</button></center></td></tr>'''
        
    myhtml += '''
<tr><td colspan="4"><img src="/hanging-office-file-folders.png" alt="Hanging File Folders" /></td></tr></table>
<hr /><br />
<button id="lookup" name="lookup" onclick="location.href='/lookup.html';">Lookup another</button>
<br /><br />
<button name="menu" onclick="location.href='/menu.html';">Home (Menu)</button><br />
</body></html>'''
    
    w('\nClosing this file.\n')
    w('-' * 66)
    w('\n')
    myfile.close()
   
    print('Content-type: text/html\n\n')
    print(myhtml)
    
    return 0 # We don't ever get here, so why not?


def lookup_in_database(searchterm: str):
    '''This sub looks the search term in all 8 fields of each record '''
    
    fields_simple = [ 'fileid','sd','ld','owner','comments' ]
    fields_complicated = [ 'lo','dt','cr' ]
    # Explanation: these three are encoded in some way.
    # lo is a 2-digit code, dt and cr are dates stored in '%Y-%m-%d' format.
    # So these three require extra processing
    
    con = sqlite3.connect(db)
    cur = con.cursor()
    
    lst = []
    fileids = set()
    # Try the uncomplicated ones first
    s = searchterm # to simplify typing and reading.
    w(f'\n\nDoing a search on {s}\n\n')
    
    for field in fields_simple:
        w(f'\t{field = }\n')
        sql = f'SELECT * FROM newfiles WHERE {field} LIKE "%{s}%"'
        cur.execute(sql)
        l = cur.fetchall()
        w(f'\n{sql = }\nlen(l)={len(l)}\n')
        for tup in l:
            fileid = tup[0]
            if fileid not in fileids:
                w(f'...adding {fileid} to list\n')
                lst.append(tup)
                fileids |= { fileid }
        w(f'After {field}:\n')
        w(f'\n\n{lst = }\n\n')
        w('\n')
    w(f'\n>>> After "simple" fields:\n{lst = }\n')
    # Now, the rest of the fields:

    # Location:
    for code,locat in locations.items():
        if s in locat.lower():
            w(f'Found a match: {locat} = {code}\n')
            sql = f'SELECT * FROM newfiles WHERE lo = "{code}"'
            cur.execute(sql)
            l = cur.fetchall()
            for tup in l:
                fileid = tup[0]
                if fileid not in fileids:
                    lst.append(tup)
                    fileids |= { fileid }

    # Creation date
    w(f'...creation date...\n')
    sql = 'SELECT fileid, cr FROM newfiles'
    cur.execute(sql)
    l = cur.fetchall()
    for tup in l:
        # we're retrieving two fields, the second one is "cr" (creation date)
        someday = ymd2dt(tup[1])
        if s in someday:
            sql = f'SELECT * FROM newfiles WHERE fileid = {tup[0]}'
            cur.execute(sql)
            t = cur.fetchone()
            fileid = t[0]
            w('for field cr, fileid="{fileid}"\n')
            w('{fileids = }\n')
            if fileid not in fileids:
                lst.append(t)
                fileids |= { fileid }
    w(f'After creation date check, at {now()}: len(lst) is...\n{len(lst)}\n\n')
             
    # Modification date:
    sql = 'SELECT fileid, dt FROM newfiles WHERE dt IS NOT NULL'
    cur.execute(sql)
    l = cur.fetchall()
    for tup in l:
        # we're retrieving two fields,
        # the second one is "dt" (modification date)
        someday = ymd2dt(tup[1])
        if s in someday:
            sql = f'SELECT * FROM newfiles WHERE fileid = {tup[0]}'
            cur.execute(sql)
            t = cur.fetchone()
            if t[0] not in fieldids:
                lst.append(t)
                fileids |= { tup[0] }
                
    w(f'After modification date check, at {now()}: lst is...\n{lst}\n\n')
    
    if not lst:
        w('\nNo items in list...calling sorry..\n\n')
        con.close()
        sorry(searchterm) # calls sys.exit()

    if DEBUG:
        w(f'lst is {lst}\n')
        
    con.close()
#    lst.sort() # return list sorted in place.
    return sorted(lst) # return a sorted copy of the list


def main():
    w('...entered main()\n')
    rv = 0
    term = form.getvalue('term').strip().lower()
    w(f'search term is {term}\n')
    if (term == ''):
        sorry('no search term')
    else:
        lst = lookup_in_database(term)
        w(f'...in main() after db lookup at {now()}, lsn(lst) is:\n{len(lst)}\n\n')
        if lst is not None:
            rv = foundit(term, lst)
        else:
            sorry(term)
    return rv


if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging "{prog}.py" on {today} at {now()}\n\n')    
    rv = main()
    rv = 0
    sys.exit(rv)
