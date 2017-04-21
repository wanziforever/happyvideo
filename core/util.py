#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import gzip
import base64
import json
from cStringIO import StringIO
from settings import settings
import time

def get_file_from_fs(path):
    return os.path.join(settings.STORE_BASE_DIR, path)

CATEGORIES = ['tv','movie','other','entertainment', 'anime']
CATEGORIE_IDS = [1001,1004,1100,1002,1005]
CATEGORIES_SEARCH = ['tv_ext', 'entertainment_ext', 'movie_ext', 'anime_ext']

# redis queue, used to pass the user activity to local multi-recom-refresher
USER_ACTIVITY_REDIS_Q_LOCAL = 'user_activity_queue_local'

# used to pass user activity to the recom engine
USER_ACTIVITY_REDIS_Q_RECOM = 'user_activity_queue_recom'

def get_category_name_by_id(cat_id):
    try:
        index = CATEGORIE_IDS.index(int(cat_id))
        return  CATEGORIES[index]
    except:
        return None

def get_category_id_by_name(cat_name):
    try:
        index = CATEGORIES.index(cat_name)
        return  CATEGORIE_IDS[index]
    except:
        return None

def most_vender_id_list():
    start = 1001
    vender_id_list = []
    while start < 1033:
        vender_id_list.append(start)
        start = start + 1
    return vender_id_list

def convert_binary_to_vender(vender_binary):
    vender_online_list = []
    all_vender_id_list = most_vender_id_list()
    binary_vender = bin(vender_binary)[2: ][::-1]
    for i, ch in enumerate(binary_vender):
        if ch == "1":
            vender_online_list.append(all_vender_id_list[i])
    return vender_online_list

def zip_json_b64(input_obj):
    json_str = json.dumps(input_obj)
    buf = StringIO()
    with gzip.GzipFile(mode='wb', fileobj=buf) as f:
        f.write(json_str)
    compressed = buf.getvalue()
    compressed_b64 = base64.b64encode(compressed)
    return compressed_b64

def unzip_json_b64(zipped):
    strin = base64.b64decode(zipped)
    buf = StringIO(strin)
    with gzip.GzipFile(mode='rb', fileobj=buf) as f:
        rdata = f.read()
    return json.loads(rdata)

#brpop multiple from redis list queue, as much as _max one time.
def brpopm(redis_session, queue_key, _max):
    rs = redis_session
    total = rs.llen(queue_key)
    if not total:
        time.sleep(3) # simulate a block pop.
        return None
    #in case the list has been pushed more elements.
    user_msgs = rs.lrange(queue_key, 0-_max, total+100000)
    rs.ltrim(queue_key, 0, -1-_max)
    return user_msgs
