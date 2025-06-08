#!/usr/bin/env python
'''This program will receive a fileid argument as a get string, viz. "<url>?fileid=1009".
   Then it looks up that record in the files database. It displays that record.
   Later, we want this program to handle Edit and Delete requests. '''

import sys
import os
import mycgi
import sqlite3

from MyFile import *

# form = mycgi.Form()


def parse_GET():
    q = os.environ.get('QUERY_STRING','There is no query string')
    if not q.startswith('fileid='):
        # Do some kind of error message
        return None
    else:
        n = q.index('=')
        fileident = q[index:]
        return int(fileident)


def goto_oncerec(fileid):
    print("Content-Type: text/html\n\n")
    print(f'''<html><head><meta http-equiv="refresh" content="0;url=/onerec.py?fileid={fileid}">''' \
          '''</head><body> <p>Redirecting to menu.html...</p></body></html>''')





    
def main():
    fileid = parse_GET()
    if fileid:
        goto_onerec(fileid);

        
    return 0  



if __name__ == '__main__':
    rv = main()
    sys.exit(rv)



############################################################################################
myhtml='''
<!DOCTYPE html>
<head>
  <meta charset="utf-8">
  <script>

	function hello(name) {
		let s = "Hello, " + name + "!";
		return s
	}
	function today() {
		dt = new Date()
		return dt
	}
	
	function verify_del(fileid) {
		alert("He made the call to verify_del!");
		return true;
    }
	
    function verify_edit(fileid) {
		alert("He called verify_edit!");
		return false;
    }
	
  </script>
</head>  
<body>
	

  <h2>This is to test the innerHTML thing.</h2>
  	<header>Make changes or delete a record altogether</header>
	<h4>This page will lead you to edit or delete a record.</h4>
	<hr />
	<p>This is where the innerHTML stuff goes</p>
	<p id="testing"></p>
	<button onclick="st=hello('amice');getElementById('hello').innerHTML=st">Hello?</button>
	<button onclick="idoubtit('meat');">I doubt it</button>
	<p id="hello">Goodbye</p>
<!--	
	<p>This is the table for innerHTML</p>
	<table>
	  <tr><td id="question" colspan="2"></td></tr>
	  <tr><td id="fileid"></td><td id="a1"></td></tr>
	  <tr><td id="sd"></td><td id="a2"></td></tr>
	</table>
	<p>End of table</p>
	<p id="ld"></p>
	<p id="lo"></p>
	<p id="dt"></p>
	<p id="yes"></p>
	<p id="hello"></p>
	<p>End of innerHTML stuff</p>

  <p>Below is for placeholders for innerHTML</p>
  <p id="test1"></p>
  <p id="thedate"></p>
  <p>Placeholders above this line.</p>
  <button onclick="getElementById('test1').innerHTML='Howdy!';">
    Click to test</button>
  <input type="button" onclick="td=today(); getElementById('thedate').innerHTML=td;" value="The date?" />
  <input type="button" onclick="verify_edit(9990)" value="Edit" />
-->
<script>
	function idoubtit(arg1) {
		s = "I want some " + arg1 + "?";
		document.getElementById("hello").innerHTML = s;
	}

  function filler() {
	  getElementById("hello").innerHTML = "FILLER"
  }
  
</script>		
</body></html>
'''
# print('Content-type: text/html\n\n')
# print(myhtml)

