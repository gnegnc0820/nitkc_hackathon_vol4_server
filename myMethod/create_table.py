import sqlite3

conn = sqlite3.connect("db/hav4_art.db")
c = conn.cursor()

c.execute("CREATE TABLE arts (id int, explain text, image blob, name text, author text, created datetime, updated datetime)")
c.execute("CREATE TABLE post (id int, parentId int, text text, color int, shape int, good int, created datetime, updated datetime)")
c.execute("CREATE TABLE vecs (id int, vec blob, date_num int, created datetime, updated datetime)")

conn.commit()
conn.close()