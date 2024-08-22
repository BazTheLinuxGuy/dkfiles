#!/usr/bin/env python
'''This program, called from the main menu,
   replaces an html file called "entry.html"
   I did this in order to be able to automatically fill
   in the next available id. Starting at 1001, they currently
   top out at around 1050 (I think). Records in the 9000's
   are test records that can be safely deleted.
   Tuesday, July 23, 2024.
'''

import sys
import os
import sqlite3
# import mycgi

from MyFile import *

# form = mycgi.Form()
# Updated:  July 23, 2023 Tues. 5:30 PM 

def get_nextid() -> int:
    w(f'...entering get_nextid() in {prog}\n')
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = 'SELECT MAX(fileid) FROM newfiles WHERE fileid < 2000'
    cur.execute(sql)
    row = cur.fetchone()
    nextid = row[0] + 1
    if nextid >= 9000:
        nextid = 1001
    return nextid

def return_error_page(e,tup):
    myhtml=f'''
<html><body><h2 style="color: red;">You have encountered an Exception</h2>
<p>Exception: {e}</p>
<p>{tup[0]}: {tup[1]}</p>
<p>{tup[2]}</p>
<p>...and that's all we know.</p></body></html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)


def return_html(nextid: int):

    w(f'...entering return_html in {prog}, next id is {nextid}...\n')
    
    myhtml = '''
<!DOCTYPE html>
<html lang="en">
  <head>
	<meta charset="utf-8" />
	<title>Enter a record</title>
	<link rel="stylesheet" href="/css/lookup.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Sriracha&display=swap');
	
    body {
		margin-left: 50px;
		box-sizing: border-box;
		background-color: #e1e1e1;
	}
	
	header {
		display: flex; 
		background-color: rgb(75,70,70);
		color: #e1f1f1;
		font-size:10pt;
		font-family: Arial,sans-serif;
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
		margin: 12px;
	}

	a {
		text-align: left;
		padding-right: 25px;
		padding-left: 0;
		color: navy;
	}
	.main {
/*		display: flex; */
		justify-content: center;
		align-items: center;
/*		width: 50% */
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
		margin: 10px 0;
		bottom: auto;
	}
  </style></head>'''
    
    w(f'\n...succeeded in creating the myhtml header\n at {now()}\n')
    
    myhtml += f'''
  <body>
	<nav>
	  <a href="/menu.html">Home (Menu)</a>
	  <a href="/lookup.html">Look up a file</a>
	  <a href="/cgi-bin/report.py">View all files</a>
	  <a href="/change.html">Edit or Delete a file</a>
    </nav>
  	<header>This form will put new information into the sql	database</header>
	  <h2>E N T E R&nbsp;&nbsp;&nbsp;A&nbsp;&nbsp;&nbsp;R E C O R D !</h2>
	  <p Fill in the fields and see the result when you press "submit"</p>
		<form id="myform" class="myform" method="POST" action="/cgi-bin/entry.py">
		  <label for="fileid">File id:</label><br />
		  <input type="text" size="6" id="fileid" name="fileid" value={nextid} />
		  <br />
		  <label for="shortdesc">Short description:</label>
		  <br />
		  <input type="text" size="50" id="shortdesc" name="shortdesc" />
		  <br />
		  <label for="longdesc">More details:</label>
		  <br />
		  <textarea type="text" cols="50" rows="3" name="longdesc"
					id="longdesc"></textarea>
		  <br />
		  <label for="location">File location:</label>
		  <br />
		  <select name="location" id="location">
			<option value="rf">red file drawers - upper</option>
			<option value="rb">red file drawers - lower</option>
			<option value="dd">David\'s desk drawers - upper</option>
			<option value="db">David\'s desk drawers - lower</option>
			<option value="ut">under long table</option>
			<option value="cl">bedroom closet</option>
			<option value="ds">downstairs</option>
			<option value="bz">with Bryan</option>
			<option value="un">unknown</option>
			<option value="lo">lost</option>
		  </select>
		  <p>Owner:</p>
		  <input type="radio" id="david" name="owner" value="David" />
		  <label for="david">David</label><br />
		  <input type="radio" id="bryan" name="owner" value="Bryan" />
		  <label for="bryan">Bryan</label><br />
		  <input type="radio" id="both" name="owner" value="Both" />
		  <label for="both">Both</label><br />
		  <input type="radio" id="unassigned" name="owner"
				 value="Unassigned" />
		  <label for="unassigned">Unassigned</label><br />
		  <label for="comments">Comments:</label><br />
		  <input type="text" id="comments" name="comments" size="60" />
		  <br />
		  <br /><br />
		  <input type="submit" value="Submit" />
		</form>
		<hr />
		<br />
		<button name="menu" id="menu" onclick='location.href="/menu.html";'>Menu</button>
		<br />
	<div class="copy">
	  	<div class="copy-text">
	  <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
	</div>
  </div>
</body></html>'''
    
    w('created the whole damn page\n')
#    w('Is there a problem with myhtml?\n')
#    myfile.close()
#    w(f'\n\n{myhtml = }\n\n')    
#    w(f'\n{myhtml = }\n')
#    myfile.close()
    
    print('Content-type: text/html\n\n',file=sys.stdout)
    print(myhtml,file=sys.stdout)
    return 0


def return_html2(nextid: int):
    w(f'got to return_myhtml2(nextid), which is {nextid}\n')
    myhtml = f'''<html><body><h1><center>The next file id is {nextid}\n</center></h1></body></html>'''
 #   w(f'\n\n{myhtml = }\n\n')
    
    print('Content-type: text/html\n\n',file=sys.stdout)
    print(myhtml,file=sys.stdout)
    return 0

    
def main_menu():
    print('Content-Type: text/html\n\n')
    print('''<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>''')    

def change_html():
    print('Content-Type: text/html\n\n')
    print('''<html><head><meta http-equiv="refresh" content="0;url=/change.html"></head><body><p>Redirecting to change.html...</p></body></html>''')    

    
def main():
    w('in main()...\n')
    nextid = get_nextid()
    w(f'got nextid as {nextid}\n')
    w('while we are at it:\n')
    w(f'{prog = }, {today = }, etc.\n')
    rv = return_html(nextid)
    return rv

if __name__ == '__main__': 
    w('\n')
    w('-' * 66)
    w('\n')
    w(f'** Debugging {prog} on {today} at {now()}.\n\n')
    rv = main()
    sys.exit(rv)





