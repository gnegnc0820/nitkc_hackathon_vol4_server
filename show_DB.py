import sqlite3
import datetime

conn = sqlite3.connect("db/hav4_art.db")
c = conn.cursor()

arts = c.execute("select * from arts").fetchall()
post = c.execute("select * from post").fetchall()
# vecs = c.execute("select * from vecs").fetchall()

conn.commit()
conn.close()

print("arts")
for i in arts:
    print(i)

print("post")
for i in post:
    print(i)