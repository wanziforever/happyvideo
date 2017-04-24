#!/usr/bin/env python

from base_handler import DataHandler
from ..datamodel.schema import order
import time

AUTH_MODE = (
    ('lvl1_user', 'lvl2_user', 'lvl3_user'), # mode 0
    ('lvl1_user', 'lvl2_user'),              # mode 1
    ('lvl1_user', 'lvl3_user'),              # mode 2
    ('lvl2_user', 'lvl2_user'),              # mode 3
    ('lvl1_user',),                          # mode 4
    ('lvl2_user',),                          # mode 5
    ('lvl3_user',)                           # mode 6
    )
    

class Platform(object):
    WECHAT = 'wechat'
    ALIPAY = 'alipay'

class ResourceType(object):
    MOVIE = 0

class OrderStatus(object):
    CREATED = 0
    SUCCEED = 1
    FAILED = 2

def id_generator(vec1, vec2, vec3):
    time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
    return vec1 + vec2 + vec3 + str(time_id)

class HandlerGetValidOrder(DataHandler):
    __handler__ = True
    def __init__(self):
        DataHandler.__init__(self)

    def process_query(self, session, **kwargs):
        mode = kwargs['mode']
        if mode > len(AUTH_MODE):
            raise Exception("invalid auth mode %d" % mode)

        auth_users = AUTH_MODE[mode]

        lvl1_user = kwargs['lvl1_user']
        lvl2_user = kwargs['lvl2_user']
        lvl3_user = kwargs['lvl3_user']

        resourceid = kwargs['resourceid']

        interval = kwargs['interval']
        cur_ts = int(time.time())
        query = session.query(order).filter(order.status==OrderStatus.SUCCEED,
                                            order.finishtime > cur_ts-interval,
                                            order.resourceid == resourceid)
        self.compute_user_filter(query, auth_users, lvl1_user, lvl2_user, lvl3_user)
        _tuples = query.all()
        orders = []
        if not _tuples:
            return orders
            
        for _tuple in _tuples:
            orders.append(_tuple.orderid)

        return orders
        
        
    def compute_user_filter(self, query, auth_users, lvl1_user, lvl2_user, lvl3_user):
        if 'lvl1_user' in auth_users:
            print "lvl1  user  filter"
            query.filter(lvl1_user==lvl1_user)
        if 'lvl2_user' in auth_users:
            print "lvl2 user filter"
            query.filter(lvl2_user==lvl2_user)
        if 'lvl3_user' in auth_users:
            print "lvl3 user filter"
            query.filter(lvl3_user==lvl3_user)
        
        
