#!/usr/bin/env python
''' This cgi program will change or delete a file record in the database'''

# Updated on: Friday, June 28, 2024 5:00 AM	  .
# Updated: Saturday, July 13, 2024 03:59:30	 .

import os
import sys
import sqlite3
import mycgi
from collections import namedtuple

from MyFile import *

DEBUG = 0

global form
form = mycgi.Form()


def fetch_records(page_number: int, records_per_page: int) -> list:
	w('...in fetch_records()\n')
	w(f'{page_number=}, {records_per_page=}\n')
	# Calculate the offset based on the page number and records per page
	offset = (page_number - 1) * records_per_page
	# Execute the query with LIMIT and OFFSET
	sql = f'SELECT * FROM newfiles ORDER BY fileid LIMIT {records_per_page} OFFSET {offset}'
	records = dbt(sql)
	return records


def database_transaction(sql: str) -> list:
	'''This routine does a "SELECT" type sql transaction
	   and returns the result as a list of tuples.
	   A tuple represents a row of a table.'''

	w('...entered database_transaction\n')
	w(f'sql is {sql}\ndbname={db}\n')
	lst = []
	try:
		con = sqlite3.connect(db)
		cur = con.cursor()
# sql = 'SELECT * FROM newfiles ORDER BY fileid'
		cur.execute(sql)
		lst = cur.fetchall()
		if DEBUG:
			if len(lst):
				for i, item in enumerate(lst):
					w(f'{i}: {item}\n')
					w('\n')
				else:
					w('Empty\n')
		con.close()
	except sqlite3.Error as er:
		sqlite3_error(er)
	except Exception as e:
		tup = sys.exc_info()
		error_page(e)
# w(f'leaving dbt() with lst {lst}\n')
	w(f'leaving dbt() with a lst: {lst[0]}\n')
	return lst


dbt = database_transaction


def sqlite3_error():
	myhtml = '''
	<html><head><meta charset="utf-8"><title>Sqlite3 Error</title>
	<link rel="stylesheet" href="/css/entry.css" />
	<style>
	  body { text-align: left; background-color: lightblue;color: #004066;padding-left:100px; }
    header { background-color: #004066; color: #e1e1e1; padding 0 100px; }
	  img { padding: 10px 10px; }
	  button { left-margin: 100px; }
	  table, th, td { border: 2px solid black; }
	</style></head>
	<body>
	<header>Details of the sqlite3 error that we have just encountered</header>
	<nav>
	  <a href="/menu.html">Home (Menu)</a>
	  <a href="/lookup.html">Lookup</a>
	  <a href="/thankyou.html>Quit entirely</a>
	<nav>
	<h2>You have encountered an error</h2><hr />'''

	htmlstr += f'''
	<table>
	<tr><th colspan="2">Details:</th></tr>
	<tr><td>Error code:</td><td>{er.sqlite_errorcode}</td></tr>
	<tr><td>Error name:</td><td>{er.sqlite_errorname}</td></tr>
	</table>
	<p>Please contact the programmer about this issue</p>
	<hr />
	<button onclick="location.href='/menu.html';">
	 Menu</button><br />
	</body></html>'''

	print('Content-type: text/html\n\n')
	print(myhtml)
	return 1


def error_page(e):
	e_info: dict = {
		'type': type(e),  # the exception type
		'args': e.args,		# arguments stored in .args
		'estr': str(e),		# __str__ allows args to be printed directly
	}
	if not e_info['args']:
		e_info['args'] = ''
		tea = None
	else:
		tea = type(e_info['args'])

	htmlstr = '''\
	<DOCTYPE !html>
	<html><head>
	<meta charset="utf-8" />
	<title>General Error</title>
	<link rel="stylesheet" href="/css/entry.html" />
	<style>
	  body {
		text-align: left; left-margin: 100px;
		background-color: lightblue; padding: 20px 100px;
	  }
	  header {
		 background-color: darkgreen; color: #e1e1e1; padding 0 100px; font-size: 12pt;
	  }
	  h1 { color: darkgreen; text-align: left; }
	  h2 { color: black; text-align: left; left-margin: 100px; }
	  p {
		  color: black; text-align:left;
		  font-size: 16pt; left-margin: 100px;
		}
	  img { padding: 10px 10px; }
	  button { left-margin: 100px; }
	  table, th, td { border: 2px solid black; }
	  table { width: 50%; }
	  th { width: 30%; text-align: center; }
	  td { width: 30%; text-align: left; }
	</style></head><body>
	<header>Error information</header>
	<h2>You have encountered an error</h2><hr />'''

	htmlstr += f'''
	<table><thead>
	<tr><th colspan="2">Details:</th></tr>
	<tr><td>The error:</td><td>{e}</td></tr>
	<tr><td>Error type:</td><td>{type(e)}</td></tr>
	<tr><td>Error args:</td><td>{e.args}</td></tr>
	<tr><td colspan=2></td><tr>
	</table>
	<p>Please contact the programmer about this issue</p>
	<hr />
	<button onclick="location.href='/menu.html';">
	 Menu</button><br />
	</body></html>'''

	print('Content-type: text/html\n\n')
	print(htmlstr)


def sorry(searchterm):
	print('Content-type: text/html\n\n')
	print('''\
<html><head><style>body { background-color: #e1e1e1; text-align: left; }
h1 { color: darkgreen; text-align: left; }
h4 { color:black; text-align: left; }
p { color: black; text-align: left; }
	</style></head>
	<body>
	<h1>Sorry!</h1>''')
	print(f'''
	<br /><br /><h4>We couldn't find the search term '{searchterm}'</h4><br />
	<p>Please try again</p>
	<button id="change" name="change" onclick="location.href='/change.html';">
	Change</button>
	<hr /><br />
	<button name="menu" id="menu"
				  onclick="location.href='/menu.html';">
	Menu</button><br />
</body></html>
''')


def foundit(searchterm: str, lst: list):
	w('Entered foundit()\n')
	w(f'len lst is {len(lst)}\n')

	myhtml = '''
<html><head>
<meta charset="utf-8"><title>Search Results</title>
<link rel="stylesheet" href="/css/dkfiles.css" />
<style>
body {
  text-align: left; left-margin: 75px; background-color: lightblue;
  padding: 0px 30px;
}
h1 { color: darkgreen; text-align: left; }
h2 { color: black; text-align: left; left-margin: 75px; }
p { color: black; text-align:left; font-size: 16pt; left-margin: 75px; }
img { padding: 10px 10px; }
button { left-margin: 75px; }
table, th, td { border: 2px solid black; }
table { width: 75%; }
td { padding-left: 10px; }
</style></head><body>
<nav class="nav">
 <a	 class="nav" href="/menu.html">Home (Menu)</a>
 <a	 class="nav" href="/lookup.html">Lookup another record</a>
</nav>'''
	myhtml += f'''
<header>Here are the &quot;dkfiles&quot; lookup results for '{searchterm}'</header>
<h2>Here's what we found for '{searchterm}'</h2>'''
	lstlen = len(lst)
	w(f'list length: {lstlen}, list: {lst}\n')
	if lstlen == 1:
		myhtml += f'<p>We found {lstlen} match</p>'
		w('Found a match.\n')
	else:
		myhtml += f'<p>We found {lstlen} matches</p>'
		myfile.write(f'We found {lstlen} matches.\n')
	myhtml += '<table width="75%"><tr><th>File id</th><th>Contents</th><th>Location</th><th>More Details?</th></tr>'
	for i, v in enumerate(lst):
		e = eachfile = onefile._make(v)
		location = locations[e.lo]

		myhtml += f'<tr><td>{e.fileid}</td><td>{e.sd}</td><td>{location}</td>'
		myhtml += f'''<td style="align-items: center"><button onclick="location.href='/cgi-bin/onerec.py?fileid={
			e.fileid}';">GO</button></td></tr>'''
	myhtml += '''
	<tr><td colspan="4">
	<img src="/hanging-office-file-folders.png" alt="Hanging File Folders" /></td></tr>
	</table>'''

	myhtml += '''
<hr /><br />
<button id="lookup" name="lookup" onclick="location.href='/lookup.html';">Lookup</button>
<br /><br />
<button name="menu" onclick="location.href='/menu.html';">Menu</button>
<br /><br /><br />
<div class="copy">
  <div class="copy-text">
	<p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
  </div>
</div>
</body></html>'''
    
	w(f'myhtml makes sense, here are the first 50 characters:\n')
	w(f'{myhtml[0:50]}\n')
	w('We\'re about to print myhtml as a web page:\n')
	w('\nClosing this file.\n')
	w('-' * 66)
	w('\n\n')

	myfile.close()

	print('Content-type: text/html\n\n')
	print(myhtml)

	return 0  # We don't ever get here, so why not?


def get_records_with_term(term: str) -> list:
	w(f'...entered get_records_with_term(), term is {term}\n')
	lst = []
	sql = f"SELECT * FROM newfiles WHERE sd LIKE '%{term}%'"
	w(f'sql is "{sql}"\n')
	lst = dbt(sql)
	if len(lst) == 0:
		f"SELECT * FROM newfiles WHERE ld LIKE '%{term}%'"
		w(f'line 190: sql is {sql}\n')
		lst = dbt(sql)
		w(f'length of returned list is {len(lst)}\n')
		if len(lst) == 0:
			sql = f'SELECT * FROM newfiles WHERE fileid LIKE %{term}%'
			lst = dbt(sql)
			if len(lst) == 0:
				sql = f"SELECT * FROM newfiles WHERE {locations[lo]} LIKE '%{term}%'"
				lst = dbt(sql)
				if len(lst) == 0:
					sql = f"SELECT * FROM newfiles WHERE dt LIKE '%{term}%'"
					lst = dbt(sql)
					if len(lst) == 0:
						sorry(term)
	w('Here is the sql statement we just executed:\n')
	w(f'\'{sql}\'\n')
	w(f'Here is the returned list:\n')
	for counter, item in enumerate(lst):
		w(f'{counter + 1}: \'{item}\'\n')
	w('\n\n')
	return lst

# Branching back to main menu:

# first method, from microsoft copilot


def main_menu1():
	print("Content-Type: text/html\n")
	print("Location: /menu.html\n\n")  # Redirect to menu.html
	print()	 # Empty line to indicate end of headers

# second method, also from copilot


def main_menu(useless=''):
	w('OK, got a button press for main menu!\n')
	myfile.close()
	redirect = '<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>'
	print('Content-Type: text/html\n\n')
	print(redirect)
	return 0


def return_html(pageno: int, records: list):
	w(f'\n...in return_html() in change.py\n')
	
	myhtml = '<html><head><meta charset="utf-8" /><title>Make changes</title><link rel="stylesheet" href="/css/change.css"/></head>'
	
	w('We have now written the <head> section of the page to be returned.\n')

	if DEBUG > 1:
		w('at line 326, myhtml is:\n')
		w(f'\n{myhtml}\n\n')

	myhtml += f'''
<body>
<header>Make changes to or delete a record altogether</header>
<nav><a href="/menu.html">Home (Menu)</a><a href="/lookup.html">Lookup</a>
	<a href="/thankyou.html">Quit Entirely</a></nav>
<h2>This page will lead you to edit or delete a record from the database, or to cancel.</h2>
<hr />
<div class="form1">
<form method="post" action="/cgi-bin/change.py">
<p>Page: {pageno}</p>
<table>
<tr><th>File ID</th><th>Contents</th><th>Location<th>Edit</th><th>Delete</th></tr>
'''

	w('We are now going to enumerate the record from the database.\n')
	w(f'{records=}\n')

	for i, tup in enumerate(records):
		thisrec = onefile._make(tup)
		w(f'{thisrec=}\n')
		myhtml += f'''
<tr>
  <td><b>{thisrec.fileid}</b></td>
  <td>{thisrec.sd}</td>
  <td>{locations[thisrec.lo]}</td>
  <td><input type="button"
	onclick="location.href='/cgi-bin/edit.py?fileid={thisrec.fileid}';" value="Edit" /></td>
  <td><input type="button"
	onclick="location.href='/cgi-bin/confirmdel.py?fileid={thisrec.fileid}';" value="Delete" /></td>
</tr>'''

	myhtml += f'''
</table>
<hr /><br /><br />
<input type="submit" id="submit" name="submit" value="&lArr;Previous">&nbsp;
<input type="submit" id="submit" name="submit" value="Next&rArr;"><br />
<input type="hidden" id="pagenum" name="pagenum" value="{pageno+1}"/>	 
<hr /><br /><br />
<input type="submit" id="submit" name="submit" value="Home (Menu)"><br />
</form></div><br /><br /><br />
<div class="copy">
  <div class="copy-text">
	<p>&copy; 2024 Kevin R. Baumgarten, All rights reserved.</p>
  </div>
</div>
</body></html>'''

	if DEBUG > 1:
		w(f'\n\n>>> Finally: <<<\n{myhtml=}\n')
	w('...wrote the html page in return_html()\n')
	myfile.close()

	print('Content-type: text/html\n\n')
	print(myhtml)

def get_totalrecs_in_files_db() -> int:
	w('\n...in get_totalrecs_in_files_db()\n')
	try:
		con = sqlite3.connect(db)
		cur = con.cursor()
		sql = 'SELECT COUNT(*) FROM newfiles'
		w(f'about to try to cur.execute "{sql}"\n')
		cur.execute(sql)
	except sqlite3.Error as er:
		w(f'received sqlite error:\n')
		w(f'code: {er.sqlite_errorcode}: {er.sqlite_errorname}.\n')
		sqlite_error(er)
		sys.exit(er.sqlite_errorcode)
	except Exception as e:
		w(f'received an Exception: \'{e}\'\n\n')
		tup = sys.exc_info()
		w(f'{tup[0]}: {tup[1]}\n')
		error_page( )
		sys.exit(99)
		
	tup = cur.fetchone()
	con.close()
	totalrecs = tup[0]
	w(f'\n>>> {totalrecs = } <<<\n')
	return totalrecs if isinstance(totalrecs,int) else int(totalrecs)



def look_for_searchterm(term: str) -> list:
	w(f'...entered look_for_searchterm({term})\n')
	term = term.lower()
	# fields to search: fileid, sd, ld, locations[lo],	owner, comments, cr, dt
	simple_fields = ('fileid', 'sd', 'ld', 'owner', 'comments')
	complicated_fields = ('lo','cr','dt')
	
	con = sqlite3.connect(db)
	cur = con.cursor()
	lst = []
	fileids = set()
	w(f'\n\nDoing a search on {term}\n\n')

	for field in simple_fields:
		w(f'{field = }')
		sql = f'SELECT * FROM newfiles WHERE {field} LIKE "%{term}"'
		cur.execute(sql)
		l = cur.fetchall()
		for tup in l:
			fileid = tup[0]
			if fileid not in fileids:
				lst.append(tup)
				fileids |= { fileid }
	w('\n>>> After "simple" fields:\n{lst = }\n')
	# Now, the rest of the fields:

	# Location:	  
	for k,v in locations.items():
		if term in v.lower():
			sql = f'SELECT * FROM newfiles WHERE lo = "{k}"'
			cur.execute(sql)
			l = cur.fetchall()
			for tup in l:
				fileid = tup[0]
				if fileid not in fileids:
					fileids |= { fileid }					 
					lst.append(tup)


	# Creation date
	sql = 'SELECT fileid, cr FROM newfiles'
	cur.execute(sql)
	l = cur.fetchall()
	for tup in l:
		# we're retrieving two fields, the second one is "cr" (creation date)
		someday = dt2ymd(tup[1])
		if term in someday:
			sql = f'SELECT * FROM newfiles WHERE fileid = {tup[0]}'
			cur.execute(sql)
			t = cur.fetchone()
			lst.append(t)

	# Modification date:
	
	sql = 'SELECT fileid, dt FROM newfiles WHERE dt IS NOT NULL'
	cur.execute(sql)
	l = cur.fetchall()
	for tup in l:
		# we're retrieving two fields,
		# the second one is "dt" (modification date)
		someday = dt2ymd(tup[1])
		if term in someday:
			sql = f'SELECT * FROM newfiles WHERE fileid = {tup[0]}'
			cur.execute(sql)
			t = cur.fetchone()
			lst.append(t)


	if not len(lst):
		w('\nNo items in list...calling sorry..\n\n')
		con.close()
		rv = sorry(term) # calls sys.exit()
		return rv
	if DEBUG > 1:
		w(f'{lst = }\n')
	else:
		w(f'{len(lst) = }\n')
		
	con.close()
	return sorted(lst)

	
def handle_searchterm(term):
	w('\n...inside handle_searchterm()\n')
	lst = []
	try:
		if ((term == '') or (term is None)):
			w('No search term was passed in.\n')
			raise ValueError('No search term, can not continue.')
	except ValueError as e:
		error_page(e)
		
	# if we get here, we're looking for a search term.
	w(f'we\'re going to look_for_searchterm({term})\n')
	lst = look_for_searchterm(term)
	rv = foundit(term,lst)
	return rv
	

def handle_the_all_button(useless=''):
	w('\n\n...in handle_the_all_button()\n')
	rv = -1
	page_number = 1
	records_per_page = 5
	w(f'...going to call fetch_records() with {page_number = }' \
	  f' and {records_per_page = }\n')
	result = fetch_records(page_number, records_per_page)
	w(f'...got back {len(result)} records.\n')
	if (len(result)):
		w(f'Calling return_html() from All,\n')
		w(f'\twith {page_number = }, {len(result) = }\n')
		w('>>> Here we go with return_html() <<<\n')
		rv = return_html(page_number,result)
	return rv


def handle_next(nrecs: int, useless=''):
	w('\n\n...in handle_next()\n')
	rv = 99
	records_per_page = 5
	w(f'going to get the hidden page number value\n')
	h = form.getvalue('pagenum')
	page_number =  h if isinstance(h,int) else int(h)
	w(f'hidden page number value is {page_number}\n')
	rec_count = (page_number - 1) * records_per_page
	w(f'{rec_count = }\n')
	if rec_count <= nrecs:
		w(f'About to call fetch records from Next\n')
		result = fetch_records(page_number, records_per_page)
		w('...back from from fetch_records:\n')
		w(f'len(result) is {len(result)}')
		if (len(result)):
			w(f'Calling return_html from Next.\n')
			rv = return_html(page_number, result)
		else:
			page_number -= 1
			result = fetch_records(page_number, records_per_page)
			if len(result):
				rv = return_html(page_number,result)
			else:
				page_number = 1
				result = fetch_records(page_number, records_per_page)
				if len(result):
					rv = return_html(page_number,result)
	return rv


def handle_previous(totalrecs):
	w(f'\n\n...in handle_previous()\n')
	rv = 99
	records_per_page = 5
	h = form.getvalue('pagenum')
	page_number = h if isinstance(h,int) else int(h)
	w(f'page number is {page_number}\n')
	
	if (page_number >= 3):
		page_number -= 2
	else:
		page_number = 1
		
	rec_count = (page_number - 1) * records_per_page
		
	if rec_count <= totalrecs:
		result = fetch_records(page_number, records_per_page)
		if (len(result)):
			w(f'Calling return_html from Previous...\n')
			rv = return_html(page_number,result)
		else:
			if page_number > 1:
				page_number -= 1
				result = fetch_records(page_number, records_per_page)
				if (len(result)):
					w(f'Calling return_html from Previous...\n')
					rv = return_html(page_number,result)
				else:
					page_number = 1
					result = fetch_records(page_number, records_per_page)
					if (len(result)):
						w(f'Calling return_html from Previous...\n')
						rv = return_html(page_number,result)
	return rv

global srchtrm

		
def main():
	w(f'\n...in in main() of {prog}.py.\n')
	page_number: int = 1
	records_per_page: int = 5
	totalrecs = get_totalrecs_in_files_db()
	w(f'...after the call, {totalrecs = }\n\n')

	term = form.getvalue('term')
	if term:
		term = term.lower()

	button = form.getvalue('submit')
	w(f'{button = }\n')
	if 'Next' in button:
		button = 'Next'
	elif 'Previous' in button:
		button = 'Previous'
	w(f'Now, {button = }\n')

# Possible button presses for "submit":
# This could come from change.html
# or from this program calling itself.
#	1. Search	(from change.html)
#	2. All		(from change.html)
# 2.5  Browse   (from change.html)
#	3. Next		(from change.py, which writes a page with a form, with 'action="change.py"')
#	4. Previous (from change.py)
#	5. Menu		(from change.py)

	w(f'Button pressed to get here: "{button}"\n')	   
	fnargs = namedtuple('fnargs','func, arg')
	w(f'\n\nWe have a value for "{fnargs = }"\n')
	callbacks = { 'Search':	  fnargs(handle_searchterm,term), \
				  'All':	  fnargs(handle_the_all_button,''), \
                  'Browse':   fnargs(handle_the_all_button,''), \
				  'Next':	  fnargs(handle_next,totalrecs), \
				  'Previous': fnargs(handle_previous,totalrecs), \
				  'Home':	  fnargs(main_menu,''), }
	if DEBUG:
		for k,v in callbacks.items():
			w(f'{k} = {v}\n')
			
	buttons = callbacks.keys()
	w(f'\n{buttons = }\n')
	
#	 button: Could be an one of the five.
#	 Exercise the appropriate subroutine

	if button in callbacks.keys():
		c = callbacks[button]
		rv = c.func(c.arg)
	else:
		rv = main_menu()
		
	return(rv)

if __name__ == '__main__':
	w('-' * 66)
	w(f'\n...in change.py __main__, debugging on {today} at {now()}\n')
	w(f'\nabout to call {prog}.py::main()\n\n')
	rv = main()
	w(f'Exiting {prog}.py with exit code {rv}.')
	sys.exit(rv)
