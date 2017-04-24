#!/usr/bin/env python

from base_handler import DataHandler
from ..datamodel.schema import order
import time

class AuthorizeMode(object):
    MODE1 = 0 
    mode2 = 1
    mode3 = 3

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

class HandlerOrderUpdate(DataHandler):
    __handler__ = True
    def __init__(self):
        DataHandler.__init__(self)

    def process_update(self, session, **kwargs):
        mode = kwargs['mode']
        platform = kwargs['platform']
        if not platform in [Platform.WECHAT, Platform.ALIPAY]:
            raise Exception('the platform is not wechat or alipay')

        orderid = kwargs['orderid']
        #price = kwargs['price']

        if mode == "confirm":
            return self.confirm_order(session, orderid, platform)
        else:
            raise Exception('confirm worker failed, unsupport update mode %s' % mode)
            
            

    def confirm_order(self, session, orderid, platform):
        query = session.query(order).filter(order.orderid==orderid)

        # check the platform consistant,
        # currently this code is strictly constraint the service,
        # and will take it over at the first stage for leting the server
        # going smoothly.
        #_tuple = query.one()
        #if platform != _tuple.platform:
        #    raise Exception("confirm order: unmatch platform, reuqest is from "
        #                    "%s, but the order is created for %s" \
        #                    % (platform, _tuple.platform))


        # for more strictly, need to check the price, too
        _tuple = query.one()
        ts = int(time.time())
        history = _tuple.history + "-> %s confirm(%s)" % (platform, str(ts))
        query.update({order.status: OrderStatus.SUCCEED,
                      order.finishtime: ts,
                      order.history: history})

        session.commit()
        return "succeed"
        
