#!/usr/bin/env python
# encoding: utf-8

import json
import time
import tornado.web
from db import session
from schema import order
from traces import Trace
from log import debug
from result import SuccResult, FailResult
from sqlalchemy.orm.exc import NoResultFound
import ConfigParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read('trade.conf')
query_loop_interval = cf.get('common', 'query_loop_interval')
                          

class ResourceType():
    MOVIE = 0

class OrderStatus():
    CREATED = 0
    WAIT_TO_PAY = 1
    PAYED = 2

order_status_string = {
    OrderStatus.CREATED: 'CREATED',
    OrderStatus.WAIT_TO_PAY: 'WAIT_TO_PAY',
    OrderStatus.PAYED: 'PAYED'
    }

    
def get_arguments(handler, *args):
    return [handler.get_argument(i, None) for i in args]

def debug_request_enter(self, trace_num, funcinfo):
    url = self.request.uri
    params = self.request.arguments
    debug(trace_num, "%s enter: url: %s, params: %s"
          % (funcinfo, url, str(params)))


class OrderApplyHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.platform = ""
        self.domain = ""
        self.room = ""
        self.device = ""
        self.videoid = ""
        self.videoname = ""
        self.fee = ""
        self.appvercode = ""
        self.appvername = ""
        self.orderid = ""
        
    def get(self):
        debug_request_enter(self, Trace.ORDER_APPLY, "OrderApplyHandler->get()")

        (self.domain, self.room, self.device) = \
                      get_arguments(self, 'domainId', 'roomId', 'deviceId')
        (self.videoid,  self.videoname, self.fee) = \
                       get_arguments(self, 'videoId', 'videoName', 'fee')
        (self.appvercode, self.appvername) = \
                          get_arguments(self, 'appVersionCode', 'appVersionName')
        self.platform = self.get_argument('platform').lower()
        

        if self.platform not in ('wechat', 'alipay'):
            self.write(FailResult('invalid charging platform %s'
                                  % self.platform).export())
            return
        
        self.orderid = self.get_new_order()

        qr_code = ""

        try:
            if self.platform == 'wechat':
                qr_code = self.get_wechat_qr()
            else:
                qr_code = self.get_alipay_qr()
        except Exception, e:
            debug(Trace.ORDER_APPLY, "error getting qrcode, %s" % str(e))
            self.write(FailResult(str(e)).export())
            return
        
        debug(Trace.ORDER_APPLY, "qr info: %s" % qr_code)
        
        data = {
            'orderId': self.orderid,
            'qrCode': qr_code,
            'platform': self.platform,
            'queryLoopInterval': query_loop_interval
            }
        self.write(SuccResult(data).export())

    def get_new_order(self):
        orderid = self.gen_orderid(self.domain, self.room, self.device)
        
        ts = int(time.time())
        clientinfo = ("appVerCode:%s, appVerName:%s"
                      % (self.appvercode, self.appvername))
        order_table = order(
            orderid=orderid,
            resourceid=self.videoid,
            resourceinfo=self.videoname,
            resourcetype=ResourceType.MOVIE, # hardcode to Movie
            lvl1_user=self.domain,
            lvl2_user=self.room,
            lvl3_user=self.device,
            clientinfo=clientinfo,
            platform=self.platform,
            price=self.fee,
            status=OrderStatus.CREATED,
            history="created(%s)"%str(ts)
            )
        session.add(order_table)
        session.commit()

        debug(Trace.ORDER_APPLY,
              "create db record for order %s successfully" % orderid)

        return orderid
        
    def gen_orderid(self, vec1, vec2, vec3):
        time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
        return vec1 + vec2 + vec3 + str(time_id)

    def get_wechat_qr(self):
        return "http://47.90.6.240"

    def get_alipay_qr(self):
        from alipay_trade import AlipayPreCreateTrade
        from tradeorder import TradeOrder
        from goods import Goods
        from traderequest import PreCreateTradeRequest
            
        precreate_trade = AlipayPreCreateTrade()
        if not self.orderid:
            raise Exception("order is needed for creating a order")
        
        test_order = TradeOrder(self.orderid, self.videoname)
        goods = Goods(self.videoid, self.videoname,
                      1, self.fee)
        test_order.set_body(self.videoname)
        test_order.add_goods(goods)
        
        debug(Trace.ORDER_APPLY, test_order.to_string())
        
        precreate_trade.set_order(test_order)
        debug(Trace.ORDER_APPLY, precreate_trade.to_string())
        

        req = PreCreateTradeRequest(precreate_trade)
        resp = req.send()
        
        status = resp['code']
        if status != '10000':
            raise Exception("ali trade response return fail, "
                            "status code %s, subcode %s, submsg: %s"
                            % (status, resp['sub_code'], resp['sub_msg']))
        
        out_trade_no = resp['out_trade_no']
        if out_trade_no != self.orderid:
            raise Exception("wrong trade no recieved, should be"
                            "%s, but got %s" % (self.orderid, out_trade_no))
        return resp['qr_code']


class OrderConfirmHandler(tornado.web.RequestHandler):
    def post(self, platform):
        debug_request_enter(self, Trace.ORDER_CB, "OrderConfirmHandler->post()")
        
        alipay_trade_no = self.get_argument('trade_no')
        (seller_id, buyer_id, buyer_logon_id) = \
                    get_arguments(self, 'seller_id', 'buyer_id', 'buyer_logon_id')
        openid = self.get_argument('open_id')
        orderid = self.get_argument('out_trade_no')

        staus_to_be = OrderStatus.CREATED
        trade_status = self.get_argument('trade_status')
        if trade_status == 'WAIT_BUYER_PAY':
            status_to_be = OrderStatus.WAIT_TO_PAY
            debug(Trace.ORDER_CB,
                  "order confirm notification to WAIT_TO_PAY for "
                  "order %s" % orderid)
        else:
            status_to_be = OrderStatus.PAYED
            debug(Trace.ORDER_CB,
                  "order confirm notification to PAYED for "
                  "order %s" % orderid)
            
        query = session.query(order).filter(order.orderid==orderid)
        
        try:
            _tuple = query.one()
        except NoResultFound:
            debug(Trace.ORDER_CB,
                  "fail to handle the request orderid(%s), no order exist"
                  "in database" % orderid)
            self.write("fail")
            return

        cur_status = _tuple.status
        history = _tuple.history
        ts = int(time.time())

        if cur_status >= status_to_be:
            debug(Trace.ORDER_CB, "wrong status, currently is %d, but "
                  "incoming is %d" % (cur_status, status_to_be))

            self.write("fail")
            return

        # history string  has risk to overflow the database definition
        history = _tuple.history + ("-> status %s change to %s by %s(at%s)"
                                    % (order_status_string[cur_status],
                                       order_status_string[status_to_be],
                                       platform, str(ts)))
        updater = {
            order.status: status_to_be,
            order.finishtime: ts,
            order.history: history,
            order.platform: platform,
            order.thirdpartyorderid: alipay_trade_no,
            }
        info = json.dumps({
            'seller_id': seller_id,
            'buyer_id': buyer_id,
            'buyer_logon_id': buyer_logon_id,
            'open_id': openid
            })
        if status_to_be == OrderStatus.WAIT_TO_PAY:
            updater[order.waittopayinfo] = info
        elif status_to_be == OrderStatus.PAYED:
            updater[order.payinfo] = info
            
        query.update(updater)
        session.commit()
        debug(Trace.ORDER_CB,
              "successfully confirm the order %s to %s"
              % (orderid, order_status_string[status_to_be]))

        self.write('success')


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
        debug_request_enter(self, Trace.ORDER_CB,
                            "ResourceValidationHandler->get()")
        (domain, room, device, videoid) = \
                 get_arguments(self, 'domainId', 'roomId', 'deviceId', 'videoId')
        
        curts = int(time.time())
        
        auth_users = AUTH_MODE[MODE_USED]

        debug(Trace.ORDER_VALIDATE,
              "order validation for user %s, and auth mode is %s"
              % (str([domain, room, device]), str(auth_users)))
        
        query = session.query(order).filter(order.status==OrderStatus.PAYED,
                                            order.finishtime > curts-INVALID_INTERVAL,
                                            order.resourceid == videoid)
        self.compute_user_filter(query, auth_users, domain, room, device)

        orders = []
        
        try:
            _tuples = query.all()
        except NoResultFound:
            debug(Trace.ORDER_VALIDATE,
                  "no order found for query %s" % str(query))
            self.write(SuccResult([]).export())
            return

        debug(Trace.ORDER_VALIDATE,
              "%d of order has been found for query" % (len(_tuples)))
        
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


class OrderQueryHandler(tornado.web.RequestHandler):
    def get(self):
        debug_request_enter(self, Trace.ORDER_QUERY,
                            "OrderQueryHandler->get()")
        # no check for the permission of the order query operation
        orderid = self.get_argument('orderId')
        if not orderid:
            debug(Trace.ORDER_QUERY, "query order should privide a order info")
            self.write(FailResult('order info should not be empty').export())
            return
        try:
            _tuple = session.query(order).filter(order.orderid==orderid).one()
        except NoResultFound:
            debug(Trace.ORDER_QUERY, "order query, no order record found for "
                  "%s" % orderid)
            self.write(SuccResult([]).expport())
            return

        debug(Trace.ORDER_QUERY, "order query, got 1 order %s, status is %s"
              % (orderid, order_status_string[_tuple.status]))
        
        data = {
            'orderId': orderid,
            'status': _tuple.status
            }

        self.write(SuccResult(data).export())
