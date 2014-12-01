import sys
import util
import MySQLdb

util.set_utf8_to_stdio()

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

# print execute_and_fetch(db, 'select * from categorylinks where cl_from = 23 limit 10;')

for line in sys.stdin:
    id, title, desc = line[:-1].split("\t")
    res =  execute_and_fetch(db, "select * from langlinks where ll_from = %s && ll_lang = 'en';" % id)
    langlink = ""
    if len(res) > 0:
        langlink = res[0][1] + ":" + res[0][2].decode('utf-8')
    print "\t".join( [id, langlink, title, desc] )

