#!/usr/bin/env python
import os
import sys
import sqlite3
import mycgi
# from collections import namedtuple
from MyFile import *


# DEBUG = 0
# global form
form = mycgi.Form()

def get_values():
    w('in get_values()...\n')
    #   w('\n...in get_values:\n')
    fileid: int = 1001    

#    w(repr(form))
#    w('\n')

    shortdesc = longdesc = location = ''
    fid = form.getvalue("fileid")
    w(f'{fid=}, type(fid) = {type(fid)}\n')
    fileid = int(fid)
    w(f'{fileid=}, type(fileid)={type(fileid)}\n')
    w('We got the fileid.\n')
    
    sd = sqlized(form.getvalue("shortdesc"))
    if form.getvalue("longdesc"):
        ld = sqlized(form.getvalue("longdesc"))
    lo = form.getvalue("location")
    location = locations["lo"]

    
    w(f'Do we get here? after {location = }\n')
    cr = sqldate()
    dt = None
    w(f'Do we get here? after {cr = }\n')
    owner = sqlized(form.getvalue("owner"))
    comments = sqlized(form.getvalue("comments"))
    w(f'''{fileid = } {sd = }\n{ld = }\n{location = } {cr = }\n{owner = } {comments = }\n\n''')
    sql = f'''INSERT INTO newfiles VALUES({fileid},'{sd}','{ld}','{lo}','{dt}','{owner}','{comments}','{cr}')'''
    w(f'\n>>>This is the processed sql statement:<<<\n{sql}\n\n')
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
    except sqlite3.Error as se:
        w('We have encountered an sqlite3 error:\n')
        myfile.close()
#        return_error_page(se)
        sys.exit(1)
    except Exception as e:
        tup = sys.exc_info()
        w(f'We found an exception, {tup[0]}, {tup[1]}\n')
        myfile.close()
#        return_error_page(e)
        sys.exit(1)
    thisrec = onefile(fileid, sd, ld, lo, dt, owner, comments, cr)
    w(f'Returning {thisrec = }.\n')
    return thisrec

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
    thisrec = get_values()
    w(f'{thisrec = }\n')
    return_html(thisrec)

if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'NEW:  Debugging {prog} on {today} at {now()}\n\n')
    main()

