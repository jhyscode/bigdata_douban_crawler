import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='******', db='mysql')

cursor = db.cursor()

cursor.execute("select version()")

data = cursor.fetchone()

print("Database version : %s " % data)

db.close()