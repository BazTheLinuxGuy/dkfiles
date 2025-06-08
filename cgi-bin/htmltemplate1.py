import os
import sys
import sqlite3
from MyFiles import *

debug_filename = 'htmlpage1_debug.txt'
df = debug_filename

prog = os.path.basename(sys.srgv[0])

myfile = open(df, 'a')
w = myfile.write

#database_name='/var/data/files.db'
#db = database_name
#
#form = 

def get_html_page(row: tuple) -> str:
    fileid = row[0]
    shortdesc = row[1]
    longdesc = row[2]
    lo = row[3]
    dt = row[4]
    htmlpage = '''\
Content-type: text/html\n\n<head><style>
body { padding: 0 50px: background-color: lightblue; }
body {
    background-color: lightblue;
    padding: 0 50px;
}
form {
    display: table;
}
p {
    display: table-row;
    font-size: 14pt;
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
<style><script><script></head><body>'''
htmlpage += f'''\
<title>dk template</title>
<h1>This is a test of {prog}</h1>
    <title>dkeditrec</title>
    <header>Plane Jane with light blue background</header>
<body>
<h2><center>This is supposed to be returned data:</center></h2>
<hr />'''
myhtml += f'''\
<form name="form1" action="temppage.py">
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
    <input id="loc" name="loc" size="40" type="text" value="{locations[lo]}" />
  </p>
  <input type="submit" id="submit" name="submit" value="Change" />
  <input type="submit" id="submit" name="submit" value="Cancel" />
  <input type="hidden" id="hidden" name="hidden" value={prog} />
</form>
<h3><b><em>Dated: {dt}</em></b></h3>
<h3>Make changes to the record, if desired.<br />
    When done, press "Accept" or "Cancel"</h3>
<br /><hr />
<button onclick="window.location.href = \'http://10.0.0.150/menu.html\'">Menu</button>
</body></html>'''
    return htmlpage



