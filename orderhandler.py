#!/usr/bin/env python
# encoding: utf-8

"""the tornado http message handlers, these handlers are in charge to
handle the happyvideo charinge service, ``OrderApplyHandler``,
``OrderConfirmHandler`` and ``ResourceValidationHandler``. the happyvideo
system require to support alipay and wxpay trade context, but this can be
hidden from client side, the backend will provide uniform interface to handle
different third party charging service. nonetheless, there are still some
little notifications that need to be taken care of, like the alipay and wxpay
have differnet qr generation mechanism and output result. different user qr
scan action event notification mechanism, etc. the handlers some times need to
seperate handle such difference by different branck, and also try best to
give a uniform result.

``OrderApplyHandler`` is used to generate a new trade order, the new created
trade order returned to client is only stand for the local order, the handler
will also apply a thridparty trade qr information with local order together,
alipay qr information applying logic refer to alipay_trade.py, and wxpay qr
applying logic refer to wxpay_trade.py

``OrderConfirmHandler`` is used to handle the thridparty trade notification
status callabck, alipay support two kinds of callback, one is for when user
scan the qr, and one is for successful charging. wxpay only support one for
successful charing. so we need to give the order status three types of status
CREATED, WAIT_TO_PAY, PAYED, alipay will bave status change path as:
CRATED->WAIT_TO_PAY->PAYED, and wxpay will only have CREATED->PAYED.
Also the change history of the order status will be recorded in the database
history field.

``ResourceValidationHandler`` is used to validate the request user's privilege
to watch a video. because the validation mechanism currently is not stable,
but still in a range of change, i have designed a user validation mode
implementation, that we have three levels of user, lvl1_user, lvl2_user,
lvl3_user, the global validation mode variable will specify which kind of
combination of user will be used for validation, there are totally serveral
cases below with a mode index number as the identifier
    ('lvl1_user', 'lvl2_user', 'lvl3_user'), # mode 0
    ('lvl1_user', 'lvl2_user'),              # mode 1
    ('lvl1_user', 'lvl3_user'),              # mode 2
    ('lvl2_user', 'lvl2_user'),              # mode 3
    ('lvl1_user',),                          # mode 4
    ('lvl2_user',),                          # mode 5
    ('lvl3_user',)                           # mode 6
when i say mode 2, it means only do lvl1_user, and lv3_user validation.
for happyvideo service, lvl1, lvl2 and lvl3 are mapped to domain, room and
device identities.

performance tips:
tornado is a famous event driven, single thread python web framework. it has
the best performance benchmarks for web application, also because it single
thread, it has no lock consideration and performance leaking, but it is also
a little hard to write best code under the framework, it require more knowledge
for IO blcoking operation concept in mind.

currently it is hard to write such high performance application in a very short
time, we use http request module which is the blocking operation, this will
block all the other request handling, but good thing is we can deploy many
instance behand a reverse proxy, and act as multiple process or thread
application, and think the charging service will not give a performance
challenge service, the reccommended the configuration with the reverse proxy
is: 2 times of validation api tornado instance than order apply, for example,
2 orderapply instance and 4 validation instance, 2 callback confirm instance.

"""


import json
import time
import tornado.web
from db import session
from schema import order
from traces import Trace
from log import debug
from urllib import quote_plus
from result import SuccResult, FailResult
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import (DatabaseError, OperationalError, StatementError)
import traceback
import ConfigParser
import xmltodict

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read('trade.conf')
query_loop_interval = cf.get('common', 'query_loop_interval')
wx_qr_parser_url = cf.get('wxpay_trade_common', 'qr_parser_url')
                          

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
        

        if self.platform not in ('wxpay', 'alipay'):
            self.write(FailResult('invalid charging platform %s'
                                  % self.platform).export())
            return
        
        self.orderid = self.get_new_order()
        if not self.orderid:
            raise Exception("order is needed for creating a order")

        qr_code = ""

        try:
            if self.platform == 'wxpay':
                qr_code = self.get_wxpay_qr()
            else:
                qr_code = self.get_alipay_qr()
        except Exception, e:
            exc = traceback.format_exc()
            debug(Trace.ORDER_APPLY, "error getting qrcode, %s" % exc)
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
        try:
            session.commit()
        except OperationalError, e:
            session.rollback()
            raise Exception("operationalError for db, %s" % str(e))

        debug(Trace.ORDER_APPLY,
              "create db record for order %s successfully fro %s"
              % (orderid, self.platform))

        return orderid
        
    def gen_orderid(self, vec1, vec2, vec3):
        time_id = str(int(time.time()*1000))+str(int(time.clock()*1000000))
        return "trade" + str(time_id)

    def get_wxpay_qr(self):
        from wxpay_trade import WXpayTrade
        from tradeorder import WXTradeOrder
        from wxtraderequest import WXTradePayRequest
        
        trade = WXpayTrade()
        order = WXTradeOrder(self.orderid, self.videoname)
        order.set_body(self.videoname)
        order.set_fee(self.fee)
        order.set_goods_tag(self.videoname)
        order.set_product_id(self.videoid)
        trade.set_order(order)

        debug(Trace.ORDER_APPLY, order.to_string())
        debug(Trace.ORDER_APPLY, trade.to_string())

        req = WXTradePayRequest(trade)
        resp = req.send()
        if resp['return_code'].lower() != 'success':
            raise Exception("wxpay return error %s, %s"
                            % (resp['return_code'], str(resp)))
        partial_url = resp['code_url']
        qr_url = wx_qr_parser_url + "?data=" + quote_plus(partial_url)
        return qr_url
        

    def get_alipay_qr(self):
        from alipay_trade import AlipayPreCreateTrade
        from tradeorder import AliTradeOrder
        from goods import Goods
        from alitraderequest import AliPreCreateTradeRequest
            
        precreate_trade = AlipayPreCreateTrade()
        
        test_order = AliTradeOrder(self.orderid, self.videoname)
        goods = Goods(self.videoid, self.videoname,
                      1, self.fee)
        test_order.set_body(self.videoname)
        test_order.add_goods(goods)
        
        debug(Trace.ORDER_APPLY, test_order.to_string())
        
        precreate_trade.set_order(test_order)
        debug(Trace.ORDER_APPLY, precreate_trade.to_string())
        

        req = AliPreCreateTradeRequest(precreate_trade)
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
    def initialize(self):
        self.platform = ""
        self.orderid = ""
        self.resp_string_map = {
            'wxpay': {'succ': 'success', 'fail': 'fail'},
            'alipay': {'succ': 'success', 'fail': 'fail'}
            }

    def write_response(self, result='succ'):
        try:
            self.write(self.resp_string_map[self.platform][result])
        except:
            self.write("no valid result mapping")
        
        
    def post(self, platform):
        debug_request_enter(self, Trace.ORDER_CB,
                            "OrderConfirmHandler->post()")
        self.platform = platform.lower()
        if self.platform not in ('wxpay', 'alipay'):
            debug(Trace.ORDER_CB,
                  "invalid platform callback %s" % platform)
            self.write("fail")
            return
        try:
            if platform == 'alipay':
                helper = self.handle_alipay_callback()
            else:
                helper = self.handle_wxpay_callback()
        except Exception,e:
            exc = traceback.format_exc()
            debug(Trace.ORDER_CB,
                  "fail to handler %s callback, %s" % exc)
            self.write_response('fail')
            return

        if self.orderid == "":
            debug(Trace.ORDER_CB, "fail to get order from %s callback"
                  % self.platform)
            self.write_response('fail')
            return

        query = session.query(order).filter(order.orderid==self.orderid)
        
        try:
            _tuple = query.one()
        except NoResultFound:
            debug(Trace.ORDER_CB,
                  "fail to handle the request orderid(%s), no order exist "
                  "in database" % self.orderid)
            self.write("fail")
            return

        cur_status = _tuple.status
        history = _tuple.history
        ts = int(time.time())

        status_to_be = helper['to_status']
        if cur_status >= status_to_be:
            debug(Trace.ORDER_CB, "wrong status, currently is %d, but "
                  "incoming is %d" % (cur_status, status_to_be))
            self.write_response("fail")
            return

        # history string  has risk to overflow the database definition
        history = _tuple.history + ("-> status %s change to %s by %s(at%s)"
                                    % (order_status_string[cur_status],
                                       order_status_string[status_to_be],
                                       self.platform, str(ts)))

        updater = {
            order.status: status_to_be,
            order.finishtime: ts,
            order.history: history,
            #order.platform: platform,
            order.thirdpartyorderid: helper['thirdparty_trade']
            }
        
        if status_to_be == OrderStatus.WAIT_TO_PAY:
            updater[order.waittopayinfo] = helper['update_info']
        elif status_to_be == OrderStatus.PAYED:
            updater[order.payinfo] = helper['update_info']
            
        query.update(updater)
        session.commit()
        debug(Trace.ORDER_CB,
              "successfully confirm the order %s to %s"
              % (self.orderid, order_status_string[status_to_be]))

        self.write_response('succ')


    def handle_alipay_callback(self):
        """receive the alipay order success callback"""
        # currently do not handle the fail callback message,
        # since i did not ever seen a fail message, and don't know
        # what the message look like
        alipay_trade_no = self.get_argument('trade_no')
        (seller_id, buyer_id, buyer_logon_id) = \
                    get_arguments(self, 'seller_id', 'buyer_id',
                                  'buyer_logon_id')
        openid = self.get_argument('open_id')
        self.orderid = self.get_argument('out_trade_no')

        debug(Trace.ORDER_CB, "alipay callback tn:%s, orderid:%s, openid:%s"
              % (alipay_trade_no, self.orderid, openid))

        staus_to_be = OrderStatus.CREATED # will be override
        trade_status = self.get_argument('trade_status')
        
        if trade_status == 'WAIT_BUYER_PAY':
            status_to_be = OrderStatus.WAIT_TO_PAY
            debug(Trace.ORDER_CB,
                  "order confirm notification to WAIT_TO_PAY for "
                  "order %s" % self.orderid)
        else:
            status_to_be = OrderStatus.PAYED
            debug(Trace.ORDER_CB,
                  "order confirm notification to PAYED for "
                  "order %s" % self.orderid)

        info = json.dumps({
            'seller_id': seller_id,
            'buyer_id': buyer_id,
            'buyer_logon_id': buyer_logon_id,
            'open_id': openid
            })
        helper = {
            'to_status': status_to_be,
            'thirdparty_trade': alipay_trade_no,
            'update_info': info
            }

        return helper

    def handle_wxpay_callback(self):
        try:
            resp = xmltodict.parse(self.request.body)
        except Exception, e:
            exc = traceback.format_exc()
            debug(Trace.ORDER_CB, "fail to handle wxpay callback for %s" % exc)
            self.write_response('fail')
            return

        if 'xml' not in resp:
            debug(Trace.ORDER_CB,
                  "fail to handle wxpay callback, no xml tag found")
            self.write_response('fail')
            return
        
        rdata = resp['xml']
        retcode = rdata['return_code']
        if retcode.lower() != "success":
            raise Exception('the return code from wxpay is %s' %retcode)
            
        info = json.dumps({
            'open_id': rdata['openid'],
            'transaction_id': rdata['transaction_id'],
            })
            
        self.orderid = rdata['out_trade_no']
        helper = {
            'to_status': OrderStatus.PAYED,
            'thirdparty_trade': rdata['transaction_id'],
            'update_info': info
            }
        
        return helper


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
            orders.append({'orderId': t.orderid, 'status': t.status})

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
