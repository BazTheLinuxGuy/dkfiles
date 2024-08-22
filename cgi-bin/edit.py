#!/usr/bin/env python
'''This program requires a file id in the GET string, viz."edit.py?fileid=1024"'''

import sys
import os
import mycgi
import sqlite3
from MyFile import *

DEBUG = 0

def error_page(exc = None):
    w('...entered error_page()\n')
    myhtml = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf=8" />
    <title>Edit error</title>
    <link rel="stylesheet" href="/css/entry.css" />
    <style>
    body {
      background-color: black;
    }
    h1 {
      color: red;
      padding-left: 100px;
    }
    h2,h3,h4,h5 {
      color: lightblue;
      padding-left: 125px;
    }
    nav {
    background-color: lightblue;
    }
    a {
      color: #404040;
    }
  
    header {
      display: flex;
      background-color: #e1e1e1;
      color: #404040;
      font-size: 10pt
    }
    </style>
    </head><body>
    <nav>
    <a href="/menu.html">Home (Menu)</a>
    <a href="/cgi-bin/change.py">Return to change</a>
    </nav>
    <h2>You have encountered an error!</h2>
    <h4>Please try again</h4>
    </body></html>'''

    myfile.close()
    print('Content-type: text/html\n\n')
    print(myhtml)


def restofowners(owner: str) -> tuple:
    w(f'...in restofowners(), {owner = }\n')
    ownerset = { o for o in owners }
    w(f'{ownerset = }')
    for o in ownerset:
        w(f'{o} ')
    w('\n')
    try:
        ownerset.remove(owner)
    except KeyError as ke:
        w('Key Error!\n')
        print('Content-type: text/html\n\n')
        print(f'''<html><body style="background-color: #004066; color: lightblue;"><h1><center>{owner} was not found in tuple &quot;owners&quot;</center></h1></body></html>''')
        time.sleep(5)
        rv=error_page()
        return rv
    return tuple(ownerset)
        

    

def return_page(rec):
    ''' The parameter is a named tuple of the "onefile" class. See MyFile.py '''
    w('\n>>>> Here is what we\'re giving back <<<\n')
    w(f'fileid is {rec.fileid},sd: {rec.sd=}\n')
    w(f'ld: {rec.ld}, lo: {rec.lo}\n')
    w(f'Owned by: {rec.owner}\n')
    w(f'Comments: {rec.comments}\n')
    w(f'Creation date: {rec.cr}, Modification date: {rec.dt}\n')
    created = ymd2dt(rec.cr)
    w(f'{created = }\n')
    w('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n')
    
    myhtml='''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Edit record</title>
    <link rel="stylesheet" href="/css/lookup.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sriracha&display=swap');
	
    body {
      margin-left: 75px;
      box-sizing: border-box;
      background-color: #e1e1e1;
    }
    
    header {
	display: flex; 
	background-color: #004066;
	color: #e1f1f1;
	font-size:10pt;
	font-family: "Sriracha",cursive,serif;
    }	

    h1 {
	color: #004066;
    }
	
    h2 {
	color: #004066;
    }
	
    p {
	color: #004066;
	font-size: 16pt;
	margin-left: 12px;
    }

    nav {
      display: flex;
      background-color: lightblue;
    }
    a {
        text-align: left;
	padding-right: 50px;
	color: #004066;
    }
    .main {
/*	display: flex; */
	justify-content: center;
	align-items: center;
/*	width: 50% */
	color: #004066;
	padding: 20px 10px;
    }
    .main h1 {
	color: #004066;
	text-align: center;
	font-family: 'Sriracha', cursive;
	text-decoration: none;
	margin-left: 75px;
    }
    .main p {
      color: #004066;
      font-size: 20px;
      text-align: left;
      font-family: 'Sriracha', cursive;
      left-margin: 75px;
    }
    .copy {
	position: relative;
	justify-content: left;
	align-items: bottom;
	padding: 0px 20px;
    }
    .copy-text p {
      position: absolute;
      font-size: 7pt;
      font-weight: bold;
      color: black;
      margin-top: 50px
      margin-left: 0;
      bottom: auto;
   }
  </style></head>
  <body>
    <nav>
      <a href="/menu.html">Home (Menu)</a>
      <a href="/lookup.html">Look up a file</a>
      <a href="/report.html">View all files</a>
    </nav>
    <header>This form will put new information into the sql
  	  database</header>
     <div id="rowcount"></div>
     <h2>E D I T&nbsp;&nbsp;&nbsp;F I L E !</h2>
     <p>Just fill in the fields and we&apos;ll see the result when
	you press "submit"</p>'''
    
    myhtml += f'''
    <form id="myform" class="myform" method="POST" action="/cgi-bin/saverec.py">
      <label for="fileid">File id:</label><br />
      <input type="text" size="6" id="fileid" name="fileid" value="{rec.fileid}" />
      <br />
      <label for="sd">Short description:</label>
      <br />
      <input type="text" size="50" id="sd" name="sd" value="{rec.sd}"/>
      <br />
      <label for="ld">More details:</label>
      <br />
      <textarea type="text" cols="50" rows="3" name="ld"
    	id="ld">{rec.ld}</textarea>
      <br />
      <label for="location">File location:</label>
      <br />'''


    loc = rec.lo
    if loc is None:
        loc = "un"
        
    location = locations[loc]
    w(f'in the middle of "return_page"...\n')
    w(f'lo is "{loc}", location id "{location}"\n')
    
    myhtml += f'''
    <input type="hidden" id="hidden" name="hidden" value="{loc}" />
    <select name="location" id="location">
      <option value="{loc}" selected>{locations[loc]}</option>'''
    
    w('...entering "for locations loop:"')
    for l,locat in locations.items():
        w(f'{l = }, {locat = }\n')
        myhtml += f'<option value="{l}">{locat}</option>'
        
    w('End of for-loop\n\n')
    myhtml += f'''
    </select>
    <br />
    <label for="cr">Written: </label><br />
    <input type="text" size="20" name="cr" id="cr" value="{created}" /><br />
    <label for="dt">Updated: </label><br />
    <input type="text" size="20" name="dt" id="dt" value="{today}" />
    <p style="font-family: "Sriracha",cursive; font-size: 12pt; color: purple;">
    <em>(The Update date has been automatically saved as today&apos;s date)</em></p>
    <br />'''

    if rec.owner is not None:
        myhtml += f'''
    <p>Owner: {rec.owner}</p>
    <input type="radio" id="owner" name="owner" value="{rec.owner}" />
    <label for="owner">{rec.owner}</label><br />'''
        others = restofowners(rec.owner)    
    else:
        myhtml += '<p>Owner: No one yet</p>'
        others = owners
    for o in others:
        myhtml += f'''    
    <input type="radio" id="owner" name="owner" value="{o}" />
    <label for="owner">{o}</label><br />'''
        
    myhtml += f'''<br />
    <label for="comments">Comments:</label><br />
    <input type="text" id="comments" name="comments" size="60" value="{rec.comments}" />'''
    myhtml += '''
    <br />
    <br /><br />
    <input type="submit" name="submit" value="Save" />&nbsp;<input type="submit" name="submit" value="Cancel" />
    </form>
    <hr />
    <br />
    <button id="back" name="back" onclick="history.back();">Back</button>&nbsp;
    <button name="menu" id="menu" onclick='location.href="/menu.html";'>Home</button><br />
    <div class="copy">
      <div class="copy-text">
        <p>&copy; 2024 Kevin R. Baumgarten, All rights reserved.</p>
      </div>
    </div>
</body></html>'''
    
    myfile.close()
    print('Content-type: text/html\n\n')
    print(myhtml)


def get_fileid() -> int:
    w('...entered get_fileid()\n')
    q = os.environ.get('QUERY_STRING','There is no query string')
    w(f'Query String = {q}\n')    
    if not q.startswith('fileid='):
        # Do some kind of error message
        w('** We errored out on the fileid retrieval.\n')
#        myfile.close()
        error_page()
        return 1
    else:
        w(f'we found a QUERY STRING in get_fileid(): {os.getenv("QUERY_STRING")}\n')
        n = q.index('=')
        w(f'{n = }\n')
        fileident = q[n+1:]
        w('{fileident = }\n')
        return int(fileident)

def fetch_record(fid: int):
    w(f'\n...entered fetch_record()\n')
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        sql = f'SELECT * FROM newfiles WHERE fileid = {fid}'
        cur.execute(sql)
        r = cur.fetchone()
        if not r:
            error_page()
            return 1
        w('@' * 76)
        w('\n')
        w(f'@ got a row for {fid} as:\n{r}\n')
        w('@' * 76)
        w('\n')
        if DEBUG:
            x = onefile._make(r)            
            w('\n\n')
            w('+' * 80)
            w('\n')
            w(f'In the sql fetch, { x.fileid = }, sd is {x.sd}\n')
            w(f'{x.ld = }\n')
            w(f'{locations[x.lo] = }, lo is {x.lo = }')
            w(f'{x.owner = }\n')
            w(f'{x.comments}\n')
            w(f'Modified: {ymd2dt(x.dt)}\n')
            w(f'Created: {ymd2dt(x.cr)}\n')
            w('+' * 80)
            w('\n\n\n')
#            del x
        w('closing the sqlite3 con object\n')
        con.close()
    except Exception as e:
        t = sys.exc_info()
        w('\nException encountered:\n')
        w(f'{t[0]}: {t[1]}\n')
        error_page()
        return 1

    x = onefile._make(r)
    return x          # pass it a named tuple instead of an unwieldy dataclass        
        
#        dkfile = MyFile(r[0],r[1],r[2],r[3],r[4],r[5],r[6])
#        return_page(dkfile)

    
def main():
# Steps:
# 1. Get the file id from the GET string
# 2. Retrieve the record from the database
# 3. Create a namedtuple "onefile" loaded with the data
#    from the record (onefile namedtuple is defined in MyFile.py).
# 4. Call the return_page subroutine with the dkfile as a parameter.
    w('...entered main()')
    fid = get_fileid()
    w(f'Got file id as {fid} from GET string.\n')
    thisfile = makeonefile(fid)   # thisfile is a "onefile" namedtuple.
    w(f'{thisfile = }\n')
    w('Calling return_page()...\n')
    return_page(thisfile)
    return 0

if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now()}\n')
    rv = main()
