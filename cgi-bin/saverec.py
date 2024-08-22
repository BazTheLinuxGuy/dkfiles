#!/usr/bin/env python
''' This program is called by edit.py, which in turn
    is called by change.py. Its purpose is to either store the record or do nothing,
    depending on whether the user made any changes.'''


# Updated: Friday, June 28, 2024 15:39:27  .


import sys
import os
import sqlite3
import mycgi
from collections import namedtuple
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



def return_no_action():
    w('...entered return_no_action\n')
    myhtml = '''
    <!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>no action</title>
    <link rel="stylesheet" href="/css/entry.css">
    </head><body>
    <nav>
    <a href="/menu.html">Home (Menu)</a>
    <a href="/change.html">Change another record.</a>
    <a href="/lookup.html">Look up a record</a>
    </nav>
    <header>No action taken</header>    
    <h1 style="color: navy;">N o&nbsp;&nbsp;&nbsp;a c t i o n   t a k e n</h1>
    <h3>No changes were detected</h3>
    <input type="button" onclick="location.href='/menu.html';" value="Home (Menu)" />
    <hr />
    <img src="/hanging-office-file-folders.png" />
    </body></html>'''
    
    myfile.close()    
    print('Content-type: text/html\n\n')
    print(myhtml)
    


    

def return_saved_record(fileid):
    w('Got to "return_saved_record()."\n')
    myhtml = f'''
<!DOCTYPE html>
    <head>
      <meta charset="utf-8">
      <title>save record</title>
      <link rel="stylesheet" href="/css/dkfiles.css">
    </head>
    <body>
      <header>SQL database successfully updated.</header>
      <nav>
        <a href="/menu.html">Home (Menu)</a>
        <a href="/change.html">Change another record.</a>
        <a href="/lookup.html">Look up a record</a>
      </nav>
      <h1 style="color: navy;">R E C O R D&nbsp;&nbsp;&nbsp;U P D A T E D</h1>
      <h3>You have successfully updated file {fileid}</h3>
      <input type="button" onclick="history.go(-2)" value="Back" />
      <input type="button" onclick="location.href='/menu.html';" value="Home (Menu)" />
      <hr />
      <img src="/hanging-office-file-folders-1.png" />
    </body></html>'''
    
    print('Content-type: text/html\n\n')
    print(myhtml)


def main_menu():
    print('Content-Type: text/html\n\n')
    print('''<html><head><meta http-equiv="refresh" content="0;url=/menu.html"></head><body><p>Redirecting to menu.html...</p></body></html>''')    

def change_html():
    print('Content-Type: text/html\n\n')
    print('''<html><head><meta http-equiv="refresh" content="0;url=/change.html"></head><body><p>Redirecting to change.html...</p></body></html>''')    

    
def main():
    w('in main()...')

    # The use chose "Save" or "Cancel" in
    # edit.py
    
    answer = form.getvalue('submit')
    answer = answer.strip()
    w(f'{answer = }\n')
    if "cancel" in answer.lower():
        change_html()
    else:   # "save"
        try:
            w('We\'re here to update a record, the user already approved it.\n')
            fid = fileid = form.getvalue('fileid')
            w(f'>>> File id is {fid}\n')
            sd = form.getvalue("sd")
            sd = sqlized(sd)
            w(f'{sd = }\n')
            ld = form.getvalue("ld")
            ld = sqlized(ld)
            w(f'{ld = }\n<<<\n')
#            lo = form.getvalue("hidden")
#            w(f'\n>>> Got the hidden value {lo} <<<\n')
            lo = form.getvalue("location")
            w(f'{lo = }\n')
            cr = form.getvalue("cr")
            cr = sqlized(cr)
            w(f'the creation date is {cr}\n')

            dt = form.getvalue("dt")
            dt = sqlized(dt)
            w(f'the modification date is {dt}\n')
            owner = sqlized(form.getvalue("owner"))
            if not owner:
                owner = "Unassigned"
            comments = sqlized(form.getvalue("comments"))
            if not comments:
                comments = "No comments yet."

            w(f'{owner = }\n{comments = }\n\n')

            # change the dates back to "%Y-%m-%d"
            w('Going to change the dates:\n')
            w(f'Before the change, {cr = } and {dt = }\n')
         
            cr = dt2ymd(cr)
            w(f'After: {cr = }\n')
            dt = dt2ymd(dt)
            w(f'After: {dt = }\n')

            w(f'{cr = }, {dt = }\n')
            
            con=sqlite3.connect(db)
            cur=con.cursor()
            w('*' * 40)
            w('\n')
            w('After reading the fields from the form, but before updating the db:\n')
            w(f'{fid = }|{sd = }\n{ld=}\n')
            w(f'{lo = }| {owner = }\n')
            w(f'{comments = }\n')
            w(f'{cr = }')
            if dt:
                w(f'{dt = }\n\n')
            w('About to create the SQL UPDATE statement\n')
             
            sql = f'''UPDATE newfiles SET fileid={fid},sd='{sd}',ld='{ld}',lo='{lo}',dt ='{dt}',owner='{owner}',comments='{comments}',cr='{cr}' WHERE fileid = {fid}'''
            w('The suspect sql statement is:\n')
            w(f'{sql}\n')
            w(f'About to cur.execute UPDATE statement:\n{sql}\n')
            cur.execute(sql)
            w(f'Just after cur.execute\n')
            con.commit()
            return_saved_record(fid)
            return 0
        except Exception as e:
            tup = sys.exc_info()
            return_error_page(e, tup)
            return 1
    return 0


if __name__ == '__main__':
    w('-' * 66)
    w('\n')
    w(f'** Debugging {prog} on {longdate()} at {now()}.\n\n')
    rv = main()
    sys.exit(rv)
