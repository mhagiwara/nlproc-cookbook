"""
Script to add langlinks information to Wikipedia TSV file.

You need to have MySQL server set up and import the langlinks data before running this script, e.g.,

$ gzcat jawiki-20160501-langlinks.sql.gz | mysql -u username jawiki20160501

This script uses the MySQL-python library, which you can install by:

$ pip install MySQL-python
"""

import sys
import MySQLdb
import codecs

# Modify this connection info according to your environment.
DB = MySQLdb.connect(host='localhost', user='root', db='jawiki20160501')


def execute_and_fetch(db, query):
    """A helper method to execute an SQL query and return the result list of row tuples."""
    rows = []

    db.query(query)
    res = db.use_result()
    row = res.fetch_row()
    while row != ():
        rows.append(row[0])
        row = res.fetch_row()
    return rows


def main():
    """Main entrypoint of this script."""
    for line in sys.stdin:
        _id, title, desc = line[:-1].split("\t")
        sql = "select * from langlinks where ll_from = %s && ll_lang = 'en';" % _id
        res = execute_and_fetch(DB, sql)
        langlink = ""
        if len(res) > 0:
            langlink = res[0][1] + ":" + res[0][2].decode('utf-8')
        print "\t".join([_id, langlink, title, desc])

if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf_8')(sys.stdin)
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main()
