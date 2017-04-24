#!/usr/bin/env python

import tornado.web
from session import create_db_session
from schema import order
from traces import Trace
from result import SuccResult, FailResult
from log import debug
from sqlalchemy.orm.exc import NoResultFound
import time

session = create_db_session('127.0.0.1', 'root', 'root123')

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
    
def get_arguments(handler, *args):
    return [handler.get_argument(i, None) for i in args]

class OrderApplyHandler(tornado.web.RequestHandler):
    def get(self):
        debug(Trace.ORDER_APPLY, "OrderApplyHandler enter")
        (domain, room, device, videoid, videoname,
         platform, appvercode, appvername, fee) = \
         get_arguments(self, 'domainId', 'roomId', 'deviceId', 'videoId',
                       'videoName', 'platform', 'appVersionCode',
                       'appVersionName', 'fee')
        orderid = self.gen_orderid(domain, room, device)
        ts = int(time.time())
        order_table = order(
            orderid=orderid,
            resourceid=videoid,
            resourceinfo=videoname,
            resourcetype=ResourceType.MOVIE, # hardcode to Movie
            lvl1_user=domain,
            lvl2_user=room,
            lvl3_user=device,
            clientinfo=appvername,
            platform=platform,
            price=fee,
            status=OrderStatus.CREATED,
            history="created(%s)"%str(ts)
            )
        session.add(order_table)
        session.commit()

        data = {
            'orderid': orderid,
            }
        
        self.write(SuccResult(data).export())
        
    def gen_orderid(self, vec1, vec2, vec3):
        time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
        return vec1 + vec2 + vec3 + str(time_id)
        

class OrderConfirmHandler(tornado.web.RequestHandler):
    def get(self, platform):
        orderid = self.get_argument('orderid', None)
        if platform not in ('wechat', 'alipay'):
            self.write(FailResult('invalid plaform <%s>' % platform).export())
            return

        query = session.query(order).filter(order.orderid==orderid)
        try:
            _tuple = query.one()
        except NoResultFound:
            self.write(FailResult('invalid orderid, not orderid found <%s>'
                                  % orderid).export())
            return

        status = _tuple.status
        history = _tuple.history
        ts = int(time.time())
        # here will have risk that the history charactors will exceed the max length
        # of the database definition
        if status == OrderStatus.SUCCEED:
            cur_platform = _tuple.platform
            if cur_platform != platform:
                err = ("duplicated confirm, but different platform "
                       "(old: %s, new: %s)(%s)" % (cur_platform, platform, str(ts)))
            else:
                err = "duplicated confirm(%s)" % str(ts)
                
            history = history + "->" + err
            query.update({
                order.history: history
                })
            session.commit()
            self.write(FailResult(("order <%s> " % orderid) + err).export())
            return
        
        history = _tuple.history + "-> %s confirm(%s)" % (platform, str(ts))
        query.update({
            order.status: OrderStatus.SUCCEED,
            order.finishtime: ts,
            order.history: history,
            order.platform: platform
            })
        session.commit()
        self.write(SuccResult("order <%s> confirmed from %s" %
                              (str(orderid), platform)).export())

AUTH_MODE = (
    ('lvl1_user', 'lvl2_user', 'lvl3_user'), # mode 0
    ('lvl1_user', 'lvl2_user'),              # mode 1
    ('lvl1_user', 'lvl3_user'),              # mode 2
    ('lvl2_user', 'lvl2_user'),              # mode 3
    ('lvl1_user',),                          # mode 4
    ('lvl2_user',),                          # mode 5
    ('lvl3_user',)                           # mode 6
    )
MODE_USED = 0
INVALID_INTERVAL = 48 * 60 * 60
class ResourceValidationHandler(tornado.web.RequestHandler):
    def get(self):
        (domain, room, device, videoid) = \
                 get_arguments(self, 'domainId', 'roomId', 'deviceId', 'videoId')
        curts = int(time.time())
        auth_users = AUTH_MODE[MODE_USED]
        query = session.query(order).filter(order.status==OrderStatus.SUCCEED,
                                            order.finishtime > curts-INVALID_INTERVAL,
                                            order.resourceid == videoid)
        self.compute_user_filter(query, auth_users, domain, room, device)

        orders = []
        
        try:
            _tuples = query.all()
        except NoResultFound:
            self.write(SuccResult([]).export())
            return

        for t in _tuples:
            orders.append(t.orderid)

        self.write(SuccResult(orders).export())

    def compute_user_filter(self, query, auth_users, lvl1_user,
                            lvl2_user, lvl3_user):
        if 'lvl1_user' in auth_users:
            query.filter(lvl1_user==lvl1_user)
        if 'lvl2_user' in auth_users:
            query.filter(lvl2_user==lvl2_user)
        if 'lvl3_user' in auth_users:
            query.filter(lvl3_user==lvl3_user)
