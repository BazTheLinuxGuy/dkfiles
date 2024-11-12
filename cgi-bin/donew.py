#!/usr/bin/env python

# Updated: Thursday, May  9, 2024 21:42:05.

import os,sys,sqlite3
from pprint import pprint
from MyFile import *

DEBUG = 1

# def database_transaction(sql: str):

def create_new_table(table_name: str, cursor) -> int:
    rv = 0
    sql = f'CREATE TABLE {table_name} (fileid int PRIMARY KEY, ' \
        'sd VARCHAR NOT NULL, ld VARCHAR, lo VARCHAR[2], dt DATE,' \
        'owner VARCHAR,comments VARCHAR);'
    try:
        r = cursor.execute(sql)
    except Exception:
        print ('Exception encountered while trying to create the new table:')
        tup = sys.exc_info()
        print(f'{tup[0]}: {tup[1]}')
        sys.exit(99)
    if DEBUG:
        print('We got this far, the new table must have been created.')
    return rv


def get_data_from_old_table(main_table_name, cursor) -> list:
    rv = 0  # but we never change the return value
            # we assume that errors will be Exceptions and we will exit.
    sql = 'SELECT * FROM dkfiles ORDER BY id'
    try:
        c = cursor.execute(sql)
        dk = c.fetchall()
    except Exception:
        print ('Exception encountered while trying to read the old table:')
        tup = sys.exc_info()
        print(f'{tup[0]}: {tup[1]}')
        sys.exit(99)
    if DEBUG:
        print('We got this far, the old data must have been read.')
    return dk

def  transfer_from_old_to_new_table(lst: list, cursor, new_table_name: str) -> int:
    rv = 0
    for i, row in enumerate(lst):
        fileid = int(row[0])
        sd = row[1]
        ld = row[2]
        lo = row[3]
        dt = row[4]
        
        sql = f'''INSERT INTO newfiles (fileid, sd, ld, lo, dt) VALUES ({row[0]},'{row[1]}','{row[2]}','{row[3]}','{row[4]}') '''
        print(f'{sql}')

        if DEBUG:
            print('The INSERT INTO sql statement to put values into the new table is:')
            print (f'{sql}')
        try:
            c = cursor.execute(sql)
        except Exception:
            print ('Exception encountered while trying to create the new table:')
            tup = sys.exc_info()
            print(f'{tup[0]}: {tup[1]}')
            sys.exit(99)
        if DEBUG:
            print('We got this far, the data must have been ' \
                  'put into the new table.')
    return rv
            
ignoreme = r'''\
INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);'''

ignoreme2 = r'''\
"INSERT INTO table1 (column_list) SELECT (column_list) FROM table2"
'''


def list_new_database(newdbname: str, cursor) -> int:
    print(f'\n\nNew table {newdbname} created! <<<')
    print('-----------------------------------\n')
    
    sql = f'SELECT * FROM {newdbname} ORDER BY fileid'
    try:
        c = cursor.execute(sql)
        lst = c.fetchall()
    except Exception:
        print ('Exception encountered while trying to create the new table:')
        tup = sys.exc_info()
        print(f'{tup[0]}: {tup[1]}')
        sys.exit(99)
    if DEBUG:
        print('We got this far, the data must have been ' \
              'read from the new table.')
   
    print('Here are the new records:')
    print('The fields are: fileid, sd, ld, lo, dt.\n' \
          'Owner and Comment don\'t have any data yet.)')
    print()
    
    for i, row in enumerate(lst):
        print(f'{row[0]:6d}, {row[1].ljust(25)},')
        print(f'{row[2].ljust(40)}, {row[3].ljust(4)}, {row[4].ljust(32)}')
        
    print()
    print('...and that is the new table.')
    print('-' * 40)
    print()
    
    return 0



def main():
    dbname='files.db'
    main_table_name = 'dkfiles'
    new_table_name = 'newfiles'
    lst: list = []
    
    con = sqlite3.connect(f'{dbname}')
    cur = con.cursor()
    
    # kloodge put in by baz because I didn't know what else to do.
    try:
        cur.execute(f'DROP TABLE {new_table_name}')
    except sqlite3.OperationalError:
        pass
    except Exception:
        print ('Exception encountered while trying to DROP the new table:')
        tup = sys.exc_info()
        print(f'{tup[0]}: {tup[1]}')
        sys.exit(999)
    if DEBUG:
        print('We got this far, the data must have been DROPped OK.')
        
    
    # First, assume there is no "newfiles" table, and just CREATE it.
    rv = create_new_table(new_table_name,cur)
    
    # This should never happen:
    if rv:
        print('Something went wrong with creating the new table, bailing...')
        sys.exit(9)

    # Now, slurp in all the data from "dkfiles"
    lst = get_data_from_old_table(main_table_name, cur)
    
    # Now, row by row, copy all of the items read from dkfiles
    # into the new table
    rv = transfer_from_old_to_new_table(lst, cur, new_table_name)
    con.commit()

    rv = list_new_database(f'{new_table_name}',cur)

    # Finish up
    con.close()
    return 0
        

if __name__ == '__main__':
    rv = main()
    sys.exit(rv) 
    
