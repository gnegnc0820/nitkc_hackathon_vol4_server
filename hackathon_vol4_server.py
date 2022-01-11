from bottle import request, route, run, BaseRequest,get,post
import json
import pickle
from myMethod.myMethod import get_posted, add_impression,do_good,add_art

BaseRequest.MEMFILE_MAX = 1024*1024 * 30

# 投稿をparentIdを指定して返す
@get('/get/posted/<parentId>')
def posted(parentId = -1):

    data = get_posted(parentId=parentId)
    return data

# 感想？を投稿
# 投稿した感想に近い傾向の作品を返す
@post('/post/post')
def add_new_post():
    post_data = request.json
    similarId = add_impression(post_data)
    return similarId

# 作品を追加
@post('/post/art')
def add_new_art():
    post_data = request.json
    add_art(post_data)

# 感想？投稿のgoodを増加させる
@get('/get/good/<postId>')
def good(postId = -1):
    do_good(postId)

run(host='localhost', port=2525)