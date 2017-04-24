#!/usr/bin/env python

from base_handler import DataHandler
from ..datamodel.schema import order
import time

class ResourceType():
    MOVIE = 0

class OrderStatus():
    CREATED = 0
    SUCCEED = 1
    FAILED = 2

def id_generator(vec1, vec2, vec3):
    time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
    return vec1 + vec2 + vec3 + str(time_id)

class HANDLER_ORDER_CREATE(DataHandler):
    __handler__ = True
    def __init__(self):
        DataHandler.__init__(self)

    def process_query(self, session, **kwargs):
        lvl1_user = kwargs['lvl1_user']
        lvl2_user = kwargs['lvl2_user']
        lvl3_user = kwargs['lvl3_user']
        clientinfo = kwargs['clientinfo']
        price = kwargs['price']
        resourceid = kwargs['resourceid']
        
        table = order(orderid=id_generator(lvl1_user, lvl2_user, lvl3_user),
                      resourceid=resourceid,
                      resourceinfo="going to get resource info from EPG system",
                      resourcetype=ResourceType.MOVIE,
                      lvl1_user=lvl1_user,
                      lvl2_user=lvl2_user,
                      lvl3_user=lvl3_user,
                      clientinfo=clientinfo,
                      price=price,
                      status=OrderStatus.CREATED
                      )
        
        session.add(table)
        session.commit()
        return table.orderid
