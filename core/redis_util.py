#!/usr/bin/env python

import redis
import json
from settings import settings
import logging
from redis.exceptions import ConnectionError
import time
import cPickle as pickle
import threading
from common.constant import RedisMessage
from functools import wraps
import socket

logger = logging.getLogger('cache_service')

class VodRedis(redis.Redis):
    """
    1.control redis using setting settings.REDIS_ENABLE
    2.if connection error, don't repeat connection within reconnect_timer
    """
    redis_enabled = True
    reconnect_timer = 10 # second
    connection_down_timestamp = 0

    def switch(self):
        redis_enabled = settings.REDIS_ENABLE
#         logger.info("redis_enabled = %s"%redis_enabled)

    def execute_command(self, *args, **options):
        if not self.redis_enabled:
            return None
        try:
            ok_time = time.time() - (self.connection_down_timestamp 
                                        + self.reconnect_timer)
            if ok_time > 0:
                self.connection_down_timestamp = 0
                return super(VodRedis, self).execute_command(*args, **options)
            else:
                return None
        except ConnectionError, e:
            self.connection_down_timestamp = time.time()
            return None
    
    def get(self, key):
        raw_ret = super(VodRedis,self).get(key)
        if raw_ret:
            return pickle.loads(raw_ret)
        else:
            return None

    def _get_media_ids(self, value):
        media_ids = []
        if isinstance(value, dict):
            for k, v in value.items():
                    if isinstance(v, list):
                        for media in v:
                            if isinstance(media, dict) and media.has_key('id'):
                                media_ids.append(media.get('id'))

        return media_ids

    def _get_media_id_key(self, media_id):
        return media_id

    def index_media(self, media_id, key):
        ttl = 2 * 24 * 3600 # media index live 2 days, more than any api cache
        media_id_key = self._get_media_id_key(media_id)
        self.sadd(media_id_key, key)
        self.expire(media_id_key, ttl)


    def un_index_media(self, media_id):
        media_id_key = self._get_media_id_key(media_id)
        # remove api cache
        api_keys = self.smembers(media_id_key)
        if api_keys != set():
            self.delete(*api_keys)
        # remove current index
        self.delete(media_id_key)


    def set(self, key, value):
        super(VodRedis,self).set(key, pickle.dumps(value))
        # index media in cache
        #for media_id in self._get_media_ids(value):
        #    self.index_media(media_id, key)

    def hset(self, key, field, value):
        super(VodRedis, self).hset(key, field, pickle.dumps(value))
    
    def hget(self, key, field):
        raw_set = super(VodRedis, self).hget(key, field)
        if raw_set:
            return pickle.loads(raw_set)
        else:
            return None
    def mget(self, key_list):
        raw_sets = super(VodRedis, self).mget(key_list)
        ret = []
        if len(raw_sets) > 0:
            for raw in raw_sets:
                if raw: 
                    ret.append(pickle.loads(raw)) 
                else:
                    ret.append(None)
        return ret

    def hmget(self, key, field_list):
        raw_sets = super(VodRedis, self).hmget(key, field_list)
        ret = []
        if len(raw_sets) > 0:
            for raw in raw_sets:
                if raw:
                    ret.append(pickle.loads(raw))
                else:
                    ret.append(None)
        return ret

    def hgetall(self, key):
        return

    def hdel(self, key, field=[]):
        super(VodRedis, self).hdel(key, field)

    def hdelmuch(self, key, field=[]):
        super(VodRedis, self).hdel(key, *field)

    
def create_redis_session():
    return redis_session

def create_individual_redis_session(redis_host, redis_port):
    _pool = redis.ConnectionPool(host=redis_host,
                                  port=redis_port,
                                  socket_timeout=5,
                                  db=0)
    _session = VodRedis(connection_pool=_pool)
    _session.switch()
    return _session

def tellRedis(tables=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwds):
            result = fn(*args, **kwds)
            table_name = kwds['table']
            if table_name in tables:
                redis_session.publish(settings.REDIS_MEDIA_PUB_QUEUE, RedisMessage.CONFIG_UPDATED)
            return result
        return wrapper
    return decorator

def publish_hot_media(msg_type, params):
    message = {'msg_type':msg_type}
    for k, v in params.items():
        message[k]=v
    logger.info('publish_hot_media---%s'%message)
    redis_session.publish(settings.REDIS_HOT_MEDIA_PUB_QUEUE, json.dumps(message))


class RedisPubSubListener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        print item

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                # print self, "unsubscribed and finished"
                break
            if item['data'] == RedisMessage.CONFIG_UPDATED:
                from apps.share.config_utils import reload_vender_config, reload_site_config
                reload_vender_config()
                reload_site_config()
            else:
                self.work(item)


#listener = RedisPubSubListener(
#    redis.Redis(
#        host=settings.REDIS_HOST,
#        port=settings.REDIS_PORT,
#        socket_connect_timeout=15,
#        socket_keepalive=True,
#        socket_keepalive_options={
#                socket.TCP_KEEPIDLE:120,
#                socket.TCP_KEEPCNT:2,
#                socket.TCP_KEEPINTVL:30
#                }
#    ), 
#    [settings.REDIS_MEDIA_PUB_QUEUE])
#
#listener.setDaemon(True)
#listener.start()

redis_session = None
if settings.CACHE_ENABLE:
    redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST,
                                      port=settings.REDIS_PORT,
                                      socket_timeout=5,
                                      db=0)
    redis_session = VodRedis(connection_pool=redis_pool)
    redis_session.switch()

