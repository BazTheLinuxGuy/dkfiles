#!/usr/bin/python

import os
import sys
import sqlite3
import mycgi
from MyFile import *


DEBUG = 0

# globals and abbrevs
debug_output = 'editrec_debug.txt'
do = debug_output

today = thedate()
now = thetime()

db = '/var/data/files.db'
myfile = open(do,'a')
w = myfile.write
prog = os.path.basename(sys.argv[0])



def error_page(prog: str):
    myhtml=f''' \
Content-type: text/html


<html><body><h1>Error in {prog}</h1>
    <h3>No fileid was given to the program></h3>
</body><html>'''
    print(myhtml)
    


def display_page(fileno: int):
    myhtml = f''' \
Content-type: text/html\n\n
<html><body><h1>Success for {prog}</h1>
<h3>The file id passed to this program is {fileid}></h3>
</body><html>'''
    print(myhtml)

def get_fileid() -> int:
    q = os.environ.get('QUERY_STRING','There is no query string')
    i = q.index('=')
    i += 1
    fileidstr: str = q[i:]
    return int(fileidstr)

def getrowtuple(fileid: int):
    con = sqlite3.connect(db)
    cur = con.cursor()
    idstr = str(fileid)
    sql = f'SELECT * FROM dkfiles WHERE id = \'{fileid}\''
    c = cur.execute(sql)
    answer = c.fetchone()
    con.close()
    if DEBUG:
        print(f'answer type is {type(answer)}')
        print(f'row tuple should be {answer[0]}',file=sys.stderr)
#    _id = answer[0]
#    _shortdesc = answer[1]
#    _longdesc = answer[2]
#    _lo = answer[3]
#    _dt = answer[4]
#    dkfile = MyFile(_id, _shortdesc, _longdesc, _lo, _dt)
    return answer
from_stack_overflow = '''\
form  { display: table;      }
p     { display: table-row;  }
label { display: table-cell; }
input { display: table-cell; }
<form>
  <p>
    <label for="a">Short label:</label>
    <input id="a" type="text">
  </p>
  <p>
    <label for="b">Very very very long label:</label>
    <input id="b" type="text">
  </p>
</form>
'''

def print_html_page_old(row):
    fileid = row[0]
    shortdesc = row[1]
    longdesc = row[2]
    lo = row[3]
    dt = row[4]
    fileid_label = 'File id:'
    sd_label = 'Contents:'
    myhtml = f'''\
Content-type: text/html\n\n<html>
<head><style></style><script></script></head>
<body>
    <title>dkedit</title>
    <header>Plane Jane</header>
    <h3><center>This is supposed to be returned data:</center></h3>
    <hr />
    <form name="form1">
    <label for="fileid">{fileid_label}</label>
    <input type="text" style="padding: 10px 50px;" size="6" name="fileid" value={fileid} />
    <br /><label for="shortdesc">{sd_label}</label><input type="text" size="50"
    style="padding: 10px 50px;" name="shortdesc" value="{shortdesc}" /><br />
    </form></body></html>'''
    print(myhtml)

def print_html_page(row):
    fileid = row[0]
    shortdesc = row[1]
    longdesc = row[2]
    lo = row[3]
    dt = row[4]
    fileid_label = 'File id:'
    sd_label = 'Contents:'
    myhtml = '''\
Content-type: text/html\n\n<html>
<head><style>
body {
    background-color: lightblue;
    padding: 0 50px;
}
form {
    display: table;
}
p {
    display: table-row;
/*    font-size: 14pt; */
}
label {
    display: table-cell;
    font-weight: bold;
}
input {
    display: table-cell;
}
textarea {
    display: table-cell;
    colspan: 2;
}
</style><script></script></head>
<body>
    <title>dkeditrec</title>
    <header>Plane Jane with light blue background</header>
    <h2>Here is full information:</center></h2>
    <hr />'''
    myhtml += f'''\
<form name="form1" action="/cgi-bin/editconfirm.py">
  <p>
    <label for="fileid">File id:&nbsp;</label>
    <input id="fileid" name="fileid" type="text" size="40" value={fileid} />
  </p>
  <p>
    <label for="sd">Contents:&nbsp;</label>
    <input id="sd" name="sd" type="text" size="40" value="{shortdesc}" />
  </p>
  <p>
    <label for="ld">More details:&nbsp;</label><br />
    <td colspan="2" style="height: 125px;">
    <textarea id="ld" name="ld" type="textarea" cols="40">{longdesc}</textarea>
    </td>
  </p>
  <p>
    <label for="loc">File location:&nbsp;</label>
<!--    <input id="loc" name="loc" size="40" type="text" value="{locations[lo]}" /> -->
    <select id="loc" name="loc">
      <option value="{lo}" selected>{locations[lo]}</option>
      <option value="rf">red filing cabinet</option>
      <option value="dd">desk drawers</option>
      <option value="ut">under long table</option>
      <option value="ds">downstairs</option>
      <option value="bz">with Bryan</option>
      <option value="un">unknown</option>
      <option value="lo">lost</option>
    </select>
  </p>
  <input type="submit" id="submit" name="submit" value="Change" />
  <input type="submit" id="submit" name="submit" value="Cancel" />
</form>
<h3><b><em>Dated: {dt}</em></b></h3>
<h3>Make changes to the record, if desired.<br />
    When done, press "Change" or "Cancel"</h3>
<br /><hr />
<button onclick="window.location.href = \'/menu.html\'">Menu</button>
</body></html>'''
    print(myhtml)

    
def main():
#    pudb.set_trace()
    fileid: int = get_fileid()
    result = getrowtuple(fileid)
    if DEBUG:
        print('Row contents:')
        for i,v in enumerate(result):
            print(f'\t{i}: {v}')
#        print('** END OF PROCESSING **')
        print()
    print_html_page(result)
    

    
if __name__ == '__main__':
    main()



    
#    htmlpage = f'''\
#Content-type: text/html\n\n
#<html><body><h1><center>Your Query String is {q}</center></h1>
#<h3><center>The file id is {fileid}</center></h3></body></html>'''
#    print(htmlpage)
#    print(f'Content-type: text/html\n\n<html><body><h1><center>Your Query String is {q}#</center></h1><h3>The file id is {fileid}</body></html')

