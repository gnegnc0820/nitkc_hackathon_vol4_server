
import sqlite3
import datetime
import pickle
import operator

import MeCab
import numpy as np
from numpy.lib.function_base import append

# model_path = "../wiki_fasttext.pickle"
model = None
# with open(model_path, "rb") as f:
#     model = pickle.load(f)

# parentId が一致する投稿を返す
def get_posted(parentId):
    conn = sqlite3.connect("db/hav4_art.db")
    c = conn.cursor()

    # arts = c.execute("select * from arts").fetchall()
    data = c.execute(f"select * from post where parentId={parentId}").fetchall()

    conn.commit()
    conn.close()

    return data

# 感想を追加する
def add_impression(data):
    
    conn = sqlite3.connect("db/hav4_art.db")
    c = conn.cursor()

    # post_id = data["id"]
    post_id = c.execute("select max(id) as maxId from post").fetchall()[0][0] + 1
    # print("#################")
    parent_id = data["parentId"]
    post_text = data["text"]
    post_color = data["color"]
    post_good = data["good"]
    post_shape = data["shape"]

    post_time = datetime.datetime.now()

    sql = "INSERT INTO post (id,parentId,text,color,shape,good,created,updated) values(?,?,?,?,?,?,?,?)"
    c.execute(sql,(post_id,parent_id,post_text,post_color,post_shape,post_good,post_time,post_time))
    
    # table:vecs に要素を追加する
    vec = c.execute(f"select * from arts where id={parent_id}").fetchall()[0][1]
    num = c.execute(f"select * from arts where id={parent_id}").fetchall()[0][2]

    text_vec = get_vector(post_text)

    sql = f"update vecs set vec={vec+text_vec}, data_num={num+1}, updated={post_time}, where id={parent_id}"
    c.execute(sql)

    conn.commit()
    conn.close()

    return get_similar_art(text_vec, parent_id)

# tableに作品を追加する
def add_art(data):
    
    conn = sqlite3.connect("db/hav4_art.db")
    c = conn.cursor()

    # post_id = data["id"]
    art_id = c.execute("select max(id) as maxId from arts").fetchall()[0][0] + 1
    # print("#################")
    explain = data["explain"]
    image = data["image"]
    name = data["name"]
    author = data["author"]

    post_time = datetime.datetime.now()

    sql = "INSERT INTO arts (id,explain,image,name,author,created,updated) values(?,?,?,?,?,?,?)"
    c.execute(sql,(art_id,explain,image,name,author,post_time,post_time))

    # table:vecs に要素を追加する
    vec = np.empty((0,300), np.float32)
    sql = "INSERT INTO vecs (id,vec,data_num,created,updated) values(?,?,?,?,?)"
    c.execute(sql,(art_id,vec,0,post_time,post_time))

    conn.commit()
    conn.close()

def do_good(post_id):
    
    conn = sqlite3.connect("db/hav4_art.db")
    c = conn.cursor()

    # post_id = data["id"]
    good = c.execute(f"select * from post where id={post_id}").fetchall()[0][-3] + 1
    # print(good[-3])
    # print("################")
    
    now = datetime.datetime.now()
    sql = f"update post set good={good}, updated='{now}' where id={post_id}"
    # print(sql)
    c.execute(sql)
    # c.execute(f"update post set (good,updated)",(good,now))

    conn.commit()
    conn.close()


# textのベクトルを返す
def get_vector(text):
    m = MeCab.Tagger("-Ochasen")
    ng_pos = ["代名詞", "数", "非自立", "副詞可能"]
    nouns = [line.split()[0] for line in m.parse(text).splitlines()
                if ("名詞" in line.split()[-1]) 
                and all((not(s in line.split()[-1])) for s in ng_pos)]
            
    s_vec = np.empty((0,300), np.float32)
    for word in nouns:
        wv = model.wv[word]
        s_vec = np.append(s_vec, np.array([wv]), axis=0)
         
    doc_vec = np.array(np.average(s_vec, axis=0))

    return doc_vec

def get_similar_art(text_vec, parentId):
    conn = sqlite3.connect("db/hav4_art.db")
    c = conn.cursor()
    data = c.execute(f"select * from vecs where id!={parentId}").fetchall()

    cos = list()
    for d in data:
        cos.append((d[0],cosin_similarity(text_vec, d[1])))

    # vecsの要素数1->他に作品がないときに終了する
    if not cos:
        return -1
        
    cos = sorted(cos, key=operator.itemgetter(1, 0), reverse=True)

    conn.commit()
    conn.close()

    return cos[0][0]

def cosin_similarity(x, y):
    return np.dot(x, y)/(np.sqrt(np.dot(x, x))*np.sqrt(np.dot(y, y)))