import sys
import os
from dataclasses import dataclass
import sqlite3
import datetime
import time

# This notation: Friday, May 24, 2024 21:00.
# Updated: Tuesday, June 18, 2024 19:41:25  .

d = datetime.date
t = time.time

global longdate
longdate = lambda: d.today().strftime('%b %d, %Y %a')
global dtdate
dtdate = lambda: d.today()
# for backwards compatibility
# to get them to save space and store date in a standard format:
global thedate
thedate = longdate
# thedate = dtdate
global thetime
thetime = lambda: time.strftime('%H:%M:%S',time.localtime(time.time()))
global sqldate
sqldate = lambda: d.today().strftime('%Y-%m-%d')

global locations
locations = {
    'rf': 'Red file drawers - upper',
    'rb': 'Red file drawers - lower',
    'dd': 'Davids file drawers - upper',
    'db': 'Davids file drawers - lower',
    'ut': 'Underneath long table',
    'at': 'Plastic drawers on long table',
    'cl': 'In the bedroom closet',
    'ds': 'Downstairs in 214',
    'bz': 'With Bryan - on desk?',
    'un': 'Unknown location',
    'lo': 'Lost, as far as we can tell',
}

months = ('','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
owners = ['David','Bryan','Both','Someone else','Unassigned']
comma = ','
hyphen = '-'
space = ' '
tab='\t'
lf='\n'
 

@dataclass
class dkfile:
    fileid: int = 1100
    sd: str = '' # short description (contents)
    ld: str = '' # longer description (more details)
    lo: str = '' # location code (see "locations")
    dt: str = '' # date (stored in the database as "%Y-%m-%d")
    owner: str = ''
    comments: str = ''
    cr: str = ''
    
    def __repr__(self):
        return f'File id: {self.fileid}\tContents: {self.sd}\n{self.ld}\n' \
            f'Where: {locations["self.lo"]} ' \
            f'Filed: {self.cr} Owner: {self.owner}\n' \
            f'Comments: {self.comments}\n'
    
    def __str__(self):
        return f'{self.fileid}, "{self.sd}",\n"{self.ld}",\n{self.lo=},' \
               f'{self.cr},{self.owner},\n{self.comments}\n'


# an alternate method:
from collections import namedtuple
global onefile
onefile = namedtuple('onefile','fileid, sd, ld, lo, dt, owner, comments, cr')
# file id, short description, long description, location code, update date,
# owner, comments, creation date
global dkfiles
dkfiles = []

# globals and abbreviations
def progname(thing: str) -> str:
    name = os.path.basename(thing)
    if '.' in thing:
        n = name.index('.')
        name = name[0:n]
    return name

global prog
prog = progname(sys.argv[0])
global debug_file
debug_file = f'{prog}_debug.txt'
global df
df = debug_file
global database_name
database_name='/var/data/files.db'
global dbname
dbname = database_name
global db
db = database_name

global today
today = thedate()
global now
now = thetime
global myfile
myfile = open(df,'a')
global w
w = myfile.write
w(f'We opened the file {df}\n')

def sqlized(data: str) -> str:
    if not isinstance(data, str):
        w(f'type of data isn\'t str, it\'s {type(data)}, for {data}\n')
        return 'None'
    apos = "'"
    quot = '"'
    dblapos = "''"
    dblquot = '""'
    if not dblapos in data:
        data = data.replace(apos,dblapos)
    if not dblquot in data:
        data = data.replace(quot,dblquot)
    return data

def makeonefile(fileid: int):
    con = sqlite3.connect(db)
    cur = con.cursor()
    sql = f'SELECT * FROM newfiles WHERE fileid = {fileid}'
    try:
        cur.execute(sql)
    except sqlite3.Error as se:
        w('sqlite3.Error encountered.')
        w(f'Code: {se.sqlite_errorcode}: {se.sqlite_errorname}')
        raise Exception(f"{fileid} was not found in newfiles table.")
    else:
        tup = cur.fetchone()
        myrec = onefile._make(tup)
    return myrec


def ymd2dt(ymd: str) -> str:
    '''Takes a date ot the strftime format '%Y-%m-%d' and translates
       it to '%%b %d, %Y %a', 'Jun 29, 2024 Wed' '''
    w(f'\n>>> {hyphen = }\t')
    w(f'{ymd = } <<<\n\n')
    if hyphen not in ymd:
        return 'Improper date format'
    else:
        ymd = ymd.replace(hyphen,' ')
        y,m,d = ymd.split()
        y = int(y)
        m = int(m)
        d = int(d)
        dtd = datetime.date(y,m,d)
        return dtd.strftime('%b %d, %Y %a')



def dt2ymd(dt: str) -> str:
    '''Takes a date ot the strftime format '%b %d, %Y %a' and translates it to '%Y-%m-%d', '2024-06-29' '''
    if dt is None:
        return None
    if comma not in dt:
        return 'Improper date format'
    else:
        dt = dt.replace(comma,'')
        mo,day,yr,wd = dt.split()
        try:
            m = months.index(mo)
        except IndexError:
            raise IndexError(f'{mo} not found in "months" list.')

        y = int(yr)
        d = int(day)
        dtd = datetime.date(y,m,d)
        return dtd.strftime('%Y-%m-%d')
    
def pause():
    ans = input('[Enter] continues, [Ctrl-c] breaks: ')
    return ans
