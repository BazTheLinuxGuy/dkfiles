#!/usr/bin/env python

import sys
import os
import sqlite3
import mycgi
from MyFile import *

DEBUG = 1

# globals and abbreviations
debug_output = 'onerec_debug.txt'
do = debug_output

database_name = '/var/data/files.db'
db = database_name

today = thedate()
now = thetime()

myfile = open(do,'a')
w = myfile.write

prog = os.path.basename(sys.argv[0])
form = mycgi.Form()

def database_transaction(sql: str) -> list:
    w('...entered database_transaction\n')
    w(f'sql is {sql}\ndb={db}\n')
    lst: list = []
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        c = cur.execute(sql)
        lst = c.fetchall()
        w(f'\nin dbt, the {len(lst)} line lst is:\n')
        if len(lst):
            for i,item in enumerate(lst):
                w(f'{i}: {item}\n')
                w('\n')    
            con.commit()
        else:
            lst = []
            w('Empty')
        con.close()
    except sqlite3.OperationalError as soe:
        return_error_page(soe)
    except Exception:
        tup = sys.exc_info()
        w('caught an Exception in dbt...\n')
        w(f'Exception info: {tup[0]}, {tup[1]}\n')
        return_error_page(Exception)
    w(f'leaving dbt() with lst {lst}\n')
    return lst

dbt = database_transaction

def get_fileid() -> int:
    w('-' * 66)
    w('\n\n')
    w('>>> In get_fileid <<<\n')
    p = os.environ.get('QUERY_STRING','There is no query string')
    w(f'QUERY STRING should be {p}\n')
    queryterm = 'fileid'
    i = p.index(queryterm) + len(queryterm)
    w(f'index of \'=\' should be {i}\n')
    q = p[i]  # should be the = sign
    w(f'This should be an \'=\': {q}\n')
    if q != '=':
        raise RuntimeError()
    i += 1
    q = p[i:]
    w(f'The file id passed in was {q}\n')
    return int(q)

def return_error_page(e):
    e_info: dict = { 
        'type': type(e),    # the exception type
        'args': e.args,     # arguments stored in .args
        'estr': str(e),     # __str__ allows args to be printed directly
    }
    if not e_info['args']:
        e_info['args'] = ''
    tea = type(e_info['args'])
    print('Content-type: text/html\n\n')
    htmlpage = '''\
<html><head>
<style>
body { text-align: left; left-margin: 100px;
       background-color: lightblue; padding: 20px 100px; }
header { display: flex; background-color: #004066;
       color: #e1e1e1; font-size:10pt; font-family: Arial;
       align-items: left; padding: 0 20px; }
h1 { color: green; text-align: left; }
h2 { color: black; text-align: left; left-margin: 100px; }
p { color: black; text-align:left; font-size: 16pt; left-margin: 100px; }
img { padding: 10px 10px; }
button { left-margin: 100px; }
table, th, td { border: 2px solid black; }
table { width: 50%; }
th { width: 30%; text-align: center; }
td { width: 30%; text-align: center; }
</style></head>
<body>
<title>Deletion Error</title>2
<header>An error has occurred while trying to delete the record</header>
<h2>You have encountered an error</h2>
<hr />
<p>Details:</p>'''
    htmlpage += f'''\
    <table>
    <tr><td align="right">Error type:</td>
        <td align="left">{e_info["type"]}</td></tr>
    <tr><td align="right">Error args:</td>
        <td align="left:>{e_info["args"]}</td></tr>
    <tr><td align="right">Error args type:</td>
        <td align="left">{tea}</td></tr>
    <tr><td align="right">The error:</td>
        <td align="left">{e_info["estr"]}</td></tr>')
    </table>
    <p>Please contact the programmer about this issue</p>
<!-- <br /><button id="change" name="change"
            onclick="location.href=\'/change.html\';">
Edit/Delete</button> -->
    <hr />
    <button name="menu" id="menu"
            onclick="location.href=\'/menu.html\';">
Menu</button><br /></body></html>'''

def drawform(fileid):
    sql = f'SELECT * FROM dkfiles WHERE id="{fileid}"'
    w(f'sql statement in draw_form is {sql}\n')
    lst=dbt(sql)
    w('The data returned from dbt is ')
    l = len(lst)
    if not l:
        w('empty.\n')
    elif (l > 1):
        try:
            raise RuntimeError
        except RuntimeError('More than one record for unique key!'):
            return_error_page(RuntimeError)
    else:
        w('\n')
        w(f'\tSELECTed row should be {lst[0]}\n')
        w('\n')
    row = lst[0]
#    fid = row[0]
    shortdesc = row[1]
    longdesc = row[2]
    lo = row[3]
    dt = row[4]
        
    myhtml = '''\
<html><head><link rel="stylesheet" href="/dkfiles1rec.css"><style>
</style><script>
function fillitin() {
const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
"Saturday"];
const months = ["January", "February", "March", "April", "May", "June", "July",
"August", "September", "October", "November", "December"];
const d = new Date()
let month = months[d.getMonth()];
let day = d.getDate()
let year = d.getFullYear();
let dt = month + " " + day + ", " + year;
document.getElementById("getdate").innerHTML = dt
return false; }
</script></head>
<body><title>One record</title>
<header>This is what the combined format would look like: one record at a time
</header>
<div class="date">
<p class="date">
<label class="date" id="getdate" for="dt">Click this button to get the date</label>
<input class="date" id="dt" name="dt" type="button"
    onclick="return fillitin();" value="Get Date"></p></div>
<div class="main"><h2>Detailed view of this record</h2>'''
    myhtml += f'''\
<p style="font-size: 16px; font-weight: bold; align-text: left">Record {fileid}</p>
</div><div class="form1">
<form name="form1" class="form1" method="POST" action="/cgi-bin/onerecord.py">
<p class="form1">
    <label class="form1" for="fileid"/>File id:</label>
    <input class="form1" id="fileid" name="fileid" type="text"
           Value="{fileid}" /></p>
<p class="form1">
    <label class="form1" for="sd"/>Contents:</label>
    <input class="form1" id="sd" name="sd" type="text" size="60"
           Value="{shortdesc}" /></p>
<p class="form1">
    <label class="form1" for="ld"/>More details:</label>
    <input class="form1" id="ld" name="ld" type="text" size="60"
           Value="{longdesc}" /></p>
<p class="form1">
    <label class="form1" for="loc"/>File location:</label>
    <input class="form1" id="loc" name="loc" type="text" size="60"
           Value="{locations[lo]}" /></p>
<p class="form1">
    <label class="form1" for="when"/>Entered on:</label>
    <input class="form1" id="when" name="when" type="text" size="60"
           Value="{dt}" /></p>
    <hr />

    </form></div>
    <div class="nav">
    <input type="submit" id="submit" name="submit" value="Next" />
    <input type="submit" id="submit" name="submit" value="Previous" />
    <input type="submit" id="submit" name="submit" value="First" />
    <input type="submit" id="submit" name="submit" value="Last" />
    </div>
<hr /><br />
<button onclick="location.href='/menu.html';">Menu</button><br />

<div class="copy">
  <div class="copy-text">
    <p>&copy; 2024 Kevin Baumgarten, All rights reserved.</p>
  </div></div></body></html>'''
    myfile.close()
    print('Content-type: text/html\n\n')
    print(myhtml)
    

    
def main():
    w('just before get fileid.\n')
    fileid: int = get_fileid()
    w(f'fileid is {fileid}\n')
    w('just before draw form.\n')
    rv = drawform(fileid)

if __name__ == '__main__':
    sys.exit(main())
