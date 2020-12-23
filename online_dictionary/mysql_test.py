import pymysql

args = {
    "host":"localhost",
    "port":3306,
    "user":"root",
    "password":"123456",
    "database":"dict",
    "charset":"utf8"
}

db = pymysql.connect(**args)
cur = db.cursor()
sql = "select word,time from history where user_id=%s;"
cur.execute(sql,(3,))
res = cur.fetchall()
print(res[0][1])
cur.close()
db.close()
