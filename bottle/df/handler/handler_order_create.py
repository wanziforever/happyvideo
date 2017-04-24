#!/usr/bin/env python

from base_handler import DataHandler
from ..datamodel.schema import order
import time

class AuthorizeMode():
    MODE1 = 0 
    mode2 = 1
    mode3 = 3

class ResourceType():
    MOVIE = 0

class OrderStatus():
    CREATED = 0
    SUCCEED = 1
    FAILED = 2

def id_generator(vec1, vec2, vec3):
    time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
    return vec1 + vec2 + vec3 + str(time_id)

class HandlerOrderCreate(DataHandler):
    __handler__ = True
    def __init__(self):
        DataHandler.__init__(self)

    def process_insert(self, session, **kwargs):
        lvl1_user = kwargs['lvl1_user']
        lvl2_user = kwargs['lvl2_user']
        lvl3_user = kwargs['lvl3_user']
        clientinfo = kwargs['clientinfo']
        platform = kwargs['platform']
        price = kwargs['price']
        resourceid = kwargs['resourceid']
        resourceinfo = kwargs['resourceinfo']
        orderid = id_generator(lvl1_user, lvl2_user, lvl3_user)
        ts = int(time.time())
        table = order(orderid=orderid,
                      resourceid=resourceid,
                      resourceinfo=resourceinfo,
                      resourcetype=ResourceType.MOVIE, # hardcode to Movie
                      lvl1_user=lvl1_user,
                      lvl2_user=lvl2_user,
                      lvl3_user=lvl3_user,
                      clientinfo=clientinfo,
                      platform='',
                      price=price,
                      status=OrderStatus.CREATED,
                      history="created(%s)"%str(ts)
                      )
        
        session.add(table)
        print "create table succeed, before commid with the id is ", table.orderid
        session.commit()
        print "create table succeed, after commid with the id is ", table.orderid
        print 
        return orderid
