#!/usr/bin/env python
'''This program, called from the main menu,
   replaces an html file called "entry.html"
   I did this in order to be able to automatically fill
   in the next available id.

   Starting at 1001, they currently top out at around 1050 (I think).

   The 2000's are currently slated for the files in thr wooden file
   cabinet next to David's desk.

   The 6000's identify the plastic drawers stcked up on the long table.
   Obviously they are not hanging files, but that's the direction this
   application  is moving: cataloging not just files, but the plethora
   of "junque" that David has kept through the years. Much of it is
   empty space and useless items.

   Records in the 9000's are test records that can be safely deleted.

   Tuesday, July 23, 2024.

# Updated Friday, November  8, 2024 15:30
# Updated: Saturday, November  9, 2024 18:15

'''

import sys
import os
import sqlite3

try:
    from MyFile import *
except Exception:
    mytup = sys.exc_info()
    info1 = mytup[0]
    info2 = mytup[1]
    info3 = mytup[2]
    print('Content-type: text/html\n\n')
    print(f'''<DOCTYPE html><html lang="en"><head />
    <body style="background-color:darkgreen;color:white;">
    <h1>{sys.path = }</h1><p>We got the following exception:</p>
    <p>{info1}: {info2}</p><p />
    <h4>Could not find file MyFile.py or its contents</h4>
    </body></html>''')

DEBUG=0

def get_nextid() -> int:
    w(f'...entering get_nextid() in {prog}\n')
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = 'SELECT MAX(fileid) FROM newfiles WHERE fileid < 3000'
    cur.execute(sql)
    row = cur.fetchone()
    nextid = row[0] + 1
    if nextid >= 2999:
        nextid = 10000
    return nextid

def return_error_page(e,tup):
    myhtml=f'''
<html><body><h2 style="color: red;">You have encountered an Exception</h2>
<p>Exception: {str(e)}</p>
<p>{tup[0]}: {tup[1]}</p>
<p>{tup[2]}</p>
<p>...and that's all we know.</p></body></html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)
    
ignoreme='''<body><h3><center>This is a test page for newdata.py</h3>
        <p style="padding-top: 100px;">Happy belated rosh hashanah</p>'''

        
def return_html(nextid: int) -> None:
    # first, do the header
    myhtml = '''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><title>testing newdata</title>
    <link rel="stylesheet" href="/css/entry.css" /></head>'''
    
    w(f'After head: {myhtml = }\n')

    # now, the body
    myhtml+=f'''
<body><h2>E N T E R&nbsp;&nbsp;&nbsp;A&nbsp;&nbsp;&nbsp;R E C O R D !</h2>
<p>Fill in the fields and see the result when you press &quot;submit&quot;</p><form name="theform" id="theform" method="post" action="/cgi-bin/process_new.py">
<label for="fileid">File id:</label><br />
<input type="number" size="6" id="fileid" name="fileid" value="{nextid}"/><br />
<label for="shortdesc">Short description:</label><br />
<input type="text" size="50" id="shortdesc" name="shortdesc" /><br />
<label for="longdesc">More details:</label><br />
<textarea cols="50" rows="3" name="longdesc" id="longdesc" >
</textarea><br />'''
    myhtml += '''
<p>Location:</p>
<select name="location" id="location">
<option value="rf">Red file drawers - upper</option>
<option value="rb">Red file drawers - lower</option>
<option value="dd">David's file drawers - upper</option>
<option value="db">David's file drawers - lower</option>
<option value="ut">Under long table</option>
<option value="cl">Bedroom closet</option>
<option value="ds">Downstairs (in 214)</option>
<option value="bz">Bryan has it</option>
<option value="un">Location unknown</option>
<option value="lo">Lost, we think</option>
</select>
<p>Owner:</p>
<input type="radio" id="david" name="owner" value="David" />
<label for="david">David</label><br />
<input type="radio" id="bryan" name="owner" value="Bryan" />
<label for="bryan">Bryan</label><br />
<input type="radio" id="both" name="owner" value="Both" />
<label for="both">Both</label><br />
<input type="radio" id="someone" name="someone"
    value="Someone Else" />
<label for="someone">Someone Else</label><br />
<input type="radio" id="unassigned" name="owner"
	 value="Unassigned" />
<label for="unassigned">Unassigned</label><br />
<label for="comments">Comments:</label><br />
<input type="text" id="comments" name="comments" size="60" />
<br /><br />
<input type="submit" value="Submit" />
</form><hr /><br />
<button name="menu" id="menu" onclick='location.href="/menu.html";'>
Menu</button><br /><div class="copy"><div class="copy-text">
<p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
</div></div></body></html>'''
  
    print('Content-type: text/html\n\n')
    print(myhtml)



    

def return_html_save(nextid: int):

    w(f'...entering return_html in {prog}, next id is {nextid}...\n')
    
    myhtml = '''
<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8" /><title>Enter a record</title>
<link rel="stylesheet" href="/css/lookup.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
<style>
p {	color: #004066;	font-size: 16pt; margin: 12px;	}
a {	text-align: left; padding-right: 25px; padding-left: 0;	color: navy; }
.main { /*		display: flex; */
		justify-content: center; align-items: center; /* width: 50% */
		color: #004066;	padding: 20px 10px;	}
.main h1 { color: #004066; text-align: center; font-family: 'Sriracha', cursive; text-decoration: none; margin-left: 75px; }
.main p { color: #004066; font-size: 20px; text-align: left;
font-family: 'Sriracha', cursive; left-margin: 75px; }
.copy {	position: relative;	justify-content: left;	align-items: bottom;
		padding: 0px 20px; }
.copy-text p { position: absolute; font-size: 7pt; font-weight: bold;
color: black; margin: 10px 0; bottom: auto;	}
</style></head>'''
    if DEBUG:
        print(f'So far, { myhtml = }',file=sys.stderr)
        k = input('[Enter] continues, [Ctrl+c] breaks: ')
        
    w(f'\n...succeeded in creating the myhtml header\n at {now()}\n')
    
    myhtml += '''<body><nav>
	  <a href="/menu.html">Home (Menu)</a>
	  <a href="/lookup.html">Look up a file</a>
 	  <a href="/cgi-bin/report.py">View all files</a>
	  <a href="/change.html">Edit or Delete a file</a>
    </nav>
  	<header>This form will put new information into the sql	database</header>
<body>
	  <h2>E N T E R&nbsp;&nbsp;&nbsp;A&nbsp;&nbsp;&nbsp;R E C O R D !</h2>
	  <p> Fill in the fields and see the result when you press &quot;submit&quot;</p>
      <form name="myform" id="myform" method="post" action="/cgi-bin/process_new.py">
		  <label for="fileid">File id:</label><br />
		  <input type="number" size="6" id="fileid" name="fi45leid" />
		  <br />
		  <label for="shortdesc">Short description:</label>
		  <br />
		  <input type="text" size="50" id="shortdesc" name="shortdesc" />
		  <br />
		  <label for="longdesc">More details:</label>
		  <br />
		  <textarea cols="50" rows="3" name="longdesc" id="location" />
          <select name="location" id="location">
            <option value="rf">red file drawers - upper</option>
			<option value="rb">red file drawers - lower</option>
			<option value="dd">David's file drawers - upper</option>
			<option value="db">David's file drawers - lower</option>
			<option value="ut">under long table</option>
			<option value="cl">bedroom closet</option>
			<option value="ds">downstairs</option>
			<option value="bz">Bryan has it</option>
			<option value="un">Location unknown</option>
			<option value="lo">Lost, we think</option>
		  </select>
		  <p>Owner:</p>
		  <input type="radio" id="david" name="owner" value="David" />
		  <label for="david">David</label><br />
		  <input type="radio" id="bryan" name="owner" value="Bryan" />
		  <label for="bryan">Bryan</label><br />
		  <input type="radio" id="both" name="owner" value="Both" />
		  <label for="both">Both</label><br />
          <input type="radio" id="someone" name="someone"
                value="Someone Else" />
          <label for="someone">Someone Else</label><br />
    	  <input type="radio" id="unassigned" name="owner"
				 value="Unassigned" />
		  <label for="unassigned">Unassigned</label><br />
		  <label for="comments">Comments:</label><br />
		  <input type="text" id="comments" name="comments" size="60" />
		  <br /><br />
		  <input type="submit" value="Submit" />
		</form>
		<hr /><br />
		<button name="menu" id="menu" onclick='location.href="/menu.html";'>
    Menu</button><br /><div class="copy"><div class="copy-text">
	<p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
	</div></div></body></html>'''
  
    w('created the whole damn page\n')
    if DEBUG:
        print(f'So far, { myhtml = }',file=sys.stderr)
        k = input('[Enter] continues, [Ctrl+c] breaks: ')
        
#    w('Is there a problem with myhtml?\n')
#    myfile.close()
#    w(f'\n\n{myhtml = }\n\n')    
#    w(f'\n{myhtml = }\n')
#    myfile.close()
    
    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0


def return_html2(nextid: int):
    w(f'got to return_myhtml2(nextid), which is {nextid}\n')
    myhtml = f'''<html>
    <body style="background-color: #e1e1e1; color: #004066;">
    <h1 margin-top="100px";>
    <center><em>The next file id is {nextid}</em></center>
    </h1></body></html>'''
 #   w(f'\n\n{myhtml = }\n\n')
    print('Content-type: text/html\n\n')
    print(myhtml)
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
    main()

