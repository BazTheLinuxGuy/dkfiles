#!/usr/bin/env python
'''This is a program that prompt the user to choose a file id,
   so that the file id can be passed to edit.py or onerec.py in the GET string'''

import sys
import os
import sqlite3
import mycgi
from MyFile import *

form = mycgi.Form()

def return_page(term,fname,thoughts):
    w('Got to return_page()\n')
    myfile.close()

    print('Content-type: text/html\n\n')
    print(myhtml)
    return 0 # never reached, so who cares?



def main():
    w('-' * 66)
    w('\n')
    w(f'Debugging {prog} on {today} at {now}.\n')
    w(f'I hope this writes a debug file.\nI just entered main() in {prog}\n')

# Steps needed:
# Present a screen of 5 records, allow user to pick 'Edit' or 'Delete'
# edit.py needs work so that it will present a view of the chosen record.
# The user can also back out by returning Home (Menu), or, if they've already made changes,
# they can still back up by pressing "Cancel" as opposed to "Save"

# I'm going to see if I can get anywhere with change.py before beginning with this.
# baz 6/11/24 Tuesday 2:00 PM



    
    return_page(term, fname, thoughts)
    return 0

if __name__ == '__main__':
    rv=main()
