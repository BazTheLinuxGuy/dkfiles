#!/usr/bin/env python
import os
import sys
import sqlite3
import mycgi
# from collections import namedtuple
from MyFile import *


# Updated Tuesday, July 23, 2024 5:00 PM
# Updated: Wednesday, September 18, 2024 17:15 


# Globals and abbrevs:

form = mycgi.Form()
# onerec = namedtuple('onerec','fileid, sd, ld, lo, dt, owner, comments, cr')
# cf. "onefile", the same named tuple declared in the MyFile module

def enter_the_new_values():
    w('\n...in enter_the_new_values:\n')
    fileid: int = 1001
    shortdesc = longdesc = location = ''
    fid = form.getvalue("fileid")
    w(f'{fid=}, type(fid) = {type(fid)}\n')
    fileid = int(fid)
    w(f'{fileid=}, type(fileid)={type(fileid)}\n')
    sd = sqlized(form.getvalue("shortdesc"))
    if form.getvalue("longdesc"):
        ld = sqlized(form.getvalue("longdesc"))
    lo = form.getvalue("location")
    location = locations[lo]
    w(f'Do we get here? after {location = }\n')
    cr = sqldate()
    dt = None
    w(f'Do we get here? after {cr = }\n')
    owner = sqlized(form.getvalue("owner"))
    comments = sqlized(form.getvalue("comments"))
    
    w(f'''{fileid = } {sd = }\n{ld = }\n{location = } {cr = }\n{owner = } {comments = }\n\n''')

#    for i,l in enumerate(locations):
#        if l == lo:
#            loc = locations[lo]
#            break;
#    con = sqlite3.connect(db)
#     cur = con.cursor()
#    sql = f'SELECT fileid, dt, cr FROM newfiles WHERE fileid={fileid}'
#    w(f'...about to execute sql statement:\n{sql = }\n\n')
#    cur.execute(sql)
#    tup = cur.fetchone()
#    con.close()
#    w(f'Got a tuple back:\n{tup = }\n\n')
#    dt = tup[1]
#    cr = tup[2]
#     cr = sqldate()
#    w(f'{cr = }')
    sql = f'''INSERT INTO newfiles VALUES({fileid},'{sd}','{ld}','{lo}','{dt}','{owner}','{comments}','{cr}')'''
    w(f'\n>>>This is the processed sql statement:<<<\n{sql}\n\n')
#    myfile.close()
#    sys.exit(99)
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
    except sqlite3.Error as se:
        w('We have encountered an sqlite3 error:\n')
#        myfile.close()
        return_error_page(se)
        sys.exit(1)
    except Exception as e:
        tup = sys.exc_info()
        w(f'We found an exception, {tup[0]}, {tup[1]}\n')
#        myfile.close()
        return_error_page(e)
        sys.exit(1)
    thisrec = onefile(fileid, sd, ld, lo, dt, owner, comments, cr)
    w(f'Returning {thisrec = }.\n')
    return thisrec


def return_error_page(e):
    e_info: dict = {
        'estr': str(e),     # __str__ allows args to be printed directly        
        'type': type(e),    # the exception type
         'args': e.args,     # arguments stored in .args

    }
    if not e_info['args']:
        e_info['args'] = ''
    else:
        tea = type(e_info['args'])
    


    htmlpage = '''                     
<html><head><title>Error!</title><style>
    body {
      text-align: left; left-margin: 75px; background-color: lightblue;
      padding: 20px 75px;
    }
    header {
      display: flex; background-color: #004066; color: #e1e1e1;
      font-size:10pt; font-family: Arial; align-items: left; padding: 0 20px; }
    h1 { color: green; text-align: left; }
    h2 { color: black; text-align: left; left-margin: 75px; }
    p { color: black; text-align:left; font-size: 16pt; left-margin: 75px; }'
    img { padding: 10px 10px; }
    button { left-margin: 75px; }
    header {
    display: flex; background-color: #004066; color: #e1e1e1;
    font-size:10pt; font-family: Arial; align-items: left; padding: 0 20px; }
    
    table, th, td { border: 2px solid black; }
    table { width: 75%; }
    a { color: #164650; }
/*    th { text-align: center; }
    td { text-align: center; } */
    </style></head>
    <body>
    <nav><a href='/menu.html';">Home (Menu)</a></nav>
    <p>Details:</p>

    <header>An &quot;exception&quot; happened when
            you entered data just now</header>
    <h2><u><i><b>You have encountered an error</b></i></u></h2>
    <hr />
    <table>'''
    
    htmlpage += f'''\
    <tr><td>Error type:</td><td>{e_info["type"]}</td></tr>
    <tr><td>Error args:</td><td>{e_info["args"]}</td></tr>
    <tr><td>Error args type:</td><td>{tea}</td></tr>
    <tr><td>The error:</td><td>{e_info["estr"]}</td></tr>
</table>
<p>These codes may not make any sense, but they indicate a deeper problem</p>
<p>Please contact the programmer about this issue</p>
<!--    <br /><button id="change" name="change" onclick="location.href='/change.html';">
 Edit/Delete</button> -->
<hr /><br />
<button name="menu" id="menu"  onclick="location.href='/menu.html';">
Menu</button><br /></body></html>'''
       
    print('Content-type: text/html\n\n')
    print(htmlpage)

def return_html(onerec):
    w(f'...entering return_html() at {now()}.\n')
    created = ymd2dt(onerec.cr)
 
    htmlpage = '''\
    <!DOCTYPE html>
    <html><head><meta charset="utf-8" /><title>Entry Accepted</title>
    <link rel="stylesheet" href="/css/entry.css" />
    <style>
    body { padding: 10px 75px;  background-color: #e1e1e1;
           text-align: left; }
    h1 { color: darkgreen; }
    h2 { color: black; }
    p { border: box; left-margin: 10px; color: black; }
    a { color: navyblue; padding: 30px; }
    header {
    display: flex; background-color: #004066; color: #e1e1e1;
    font-size:10pt; font-family: "Georgia","Sriracha",cursive,sans-serif;
    align-items: left; padding: 5px 5px; }
    table, th, td { border: 2px solid black; }
    th { color: black; }
    td { color: navy; margin: 5px 10px; }
    </style></head><body>
    <header>Your new record can be seen in the Report page</header>
    <nav>
      <a href="/menu.html">Home (Menu)</a>
      <a href="/cgi-bin/newdata.py">Enter another record</a>
      <a href="/lookup.html">Lookup a record</a>
    </nav>
    <h1>Entry accepted.</h1>
    <h2>Your entry is now in the database.</h2>
    <table width="50%" cols="2" style="border: 2px solid black;">
    <tr><th>Field name</th><th>Value</th></tr>'''
#    if dt is None:
#        dt = 'Not yet'
    htmlpage += f'''\
    <tr><td>File Id:</td><td>{onerec.fileid}</td></tr>
    <tr><td>Contents:</td><td>{onerec.sd}</td></tr>
    <tr><td>More details:</td><td>{onerec.ld}</td></tr>
    <tr><td>Location:</td><td>{locations[onerec.lo]}</td></tr>
    <tr><td>Owner:</td><td>{onerec.owner}</td></tr>
    <tr><td>Comments:</td><td>{onerec.comments}</td></tr>
    <tr><td>Created:</td><td>{created}</td></tr>
    </table><br />
    <button onclick="location.href='/cgi-bin/newdata.py';">
    Entry Form</button><hr /><br />
    <button onclick="location.href='/menu.html';">Menu</button><br />
    <br /><br /><br />
    <div class="copy">
      <div class="copy-text">
    	<p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
      </div>
    </div>
    </body></html>'''
    
    myfile.close()
    print('Content-type: text/html\n\n')
    print(htmlpage)

def main():
    w(f'Entering main()...\n')
    thisrec = enter_the_new_values()
    w(f'{thisrec = }\n')
    return_html(thisrec)

if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now()}\n\n')
    main()
