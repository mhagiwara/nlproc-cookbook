import sys
import MySQLdb
import codecs
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)


def execute_and_fetch(db, query):
    rows = []

    db.query(query)
    res = db.use_result()
    row = res.fetch_row()
    while row != ():
        rows.append(row[0])
        row = res.fetch_row()
    return rows

db = MySQLdb.connect(host='localhost', user='root', db='jawiki20141122')

for line in sys.stdin:
    id, langlink, title, desc = line[:-1].split("\t")

    res = execute_and_fetch(db, "select cl_to from categorylinks where cl_from = %s;" % id)
    categories = [row[0].decode('utf-8') for row in res]
    desc = desc.replace("</text>", "")
    print "\t".join([id, title, langlink, " ".join(categories), desc])
