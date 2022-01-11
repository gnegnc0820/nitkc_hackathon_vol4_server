import sqlite3
import datetime

conn = sqlite3.connect("db/hav4_art.db")
c = conn.cursor()

# c.execute("CREATE TABLE arts (id int, explain text, image blob, name text, created datetime, updated datetime)")
# c.execute("CREATE TABLE post (id int, parentId int, explain text, color int, good int, created datetime, updated datetime)")

arts = c.execute("select * from arts")
post = c.execute("select * from post")

art_id = 0
art_explain = "this is explain"
art_image = None
art_name = "this is art title"
author = "author"

now = datetime.datetime.now()
sql = "INSERT INTO arts (id,explain,image,name,author,created,updated) values(?,?,?,?,?,?,?)"
c.execute(sql,(art_id,art_explain,art_image,art_name,author,now,now))


post_id = 0
parent_id = 0
post_text = "this is posted text"
post_color = 1
post_good = 4
post_shape = 1

post_time = datetime.datetime.now()

sql = "INSERT INTO post (id,parentId,text,color,shape,good,created,updated) values(?,?,?,?,?,?,?,?)"
c.execute(sql,(post_id,parent_id,post_text,post_color,post_shape,post_good,post_time,post_time))

conn.commit()
conn.close()