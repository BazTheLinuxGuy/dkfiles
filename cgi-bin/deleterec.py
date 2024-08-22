#!/usr/bin/env python
''' This program is called by confirmdel.py, which in turn
    is called by change.py'''

# Updated: Saturday, June 29, 2024 11:16:50  .

import sys
import os
import sqlite3
import mycgi
from MyFile import *

form = mycgi.Form()


def return_error_page(e,tup):
    myhtml=f'''
<html><body><h2 style="color: red;">You have encountered an Exception</h2>
<p>Exception: {e}</p>
<p>{tup[0]}: {tup[1]}</p>
<p>{tup[2]}</p>
<p>...and that's all we know.</p></body></html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)
    

def return_success_page(fileid):
    w('Got to \'return_success_page\'\n')
    myhtml = f'''
<!DOCTYPE html><head><meta charset="utf-8"><link rel="stylesheet" href="/css/dkfiles.html">
<nav><a href="/menu.html">Home (Menu)</a><a href="/change.html>
    Edit or Delete another file</a><a href="/lookup.html">Look up a record.</a></nav>
</head><body>
    <h1 style="color: navy;">S U C C E S S !</h1>
    <p>You have successfully deleted file {fileid}</p>
    <button onclick="location.href='/menu.html';">Home (Menu)</button>&nbsp;
    <button onclick="history.go(-2)">Go Back</button>
    <hr />
    <img src="/hanging-office-file-folders-1.png" />
    </body></html>'''
    print('Content-type: text/html\n\n')
    print(myhtml)

    
def main():
    w('in main()...')
    answer = form.getvalue('submit')
    answer = answer.strip()
    w(f'{answer = }\n')
    
    if ("yes" in answer.lower()):
        try:
            w('We\'re getting the fileid...\n')
            fileid = form.getvalue('fileid')
            w(f'The user chose "yes" to delete file {fileid}.\n')
            con=sqlite3.connect(db)
            cur=con.cursor()
            sql = f"DELETE FROM newfiles WHERE fileid = {fileid}"
            w(f'About to cur.execute {sql}\n')
            cur.execute(sql)
            w(f'Just after cur.execute\n')
        except Exception as e:
            tup = sys.exc_info()
            return_error_page(e, tup)
        else:
            w(f'in the "finally" block\n')
            con.commit()
            con.close()
            return_success_page(fileid)
    else:
        # else they chose "no". Return to change.html.
        w(f'OK, {answer = }\n')
        w('We got to where they picked "no".\n')
        w('Branching back to change.html\n')
        myfile.close()
        print('Content-Type: text/html\n\n')
        print('''<html><head><meta http-equiv="refresh" content="0;url=/change.html"></head><body><p>Redirecting to change.html...</p></body></html>''')    
    return 0


if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'** Debugging {prog} on {today} at {now()}.\n\n')
    rv = main()
    sys.exit(rv)
