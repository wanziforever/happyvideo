#!/usr/bin/env python

"""the aim of this script is used to check the order status, and try to help
the order which miss any thirdparty callback notifications.

to avoid the check for all the orders every time, a field need to be added to
the database ``order`` table, to indicate whether the order need to be checked
again.

since alipay has a status with WAIT_TO_PAY, and wxpay did not, alipay order
will only do a check when the order status WAIT_TO_PAY.

for the order didnot get payed for a long time, just drop it for any further
checking. also the checking mechanism is not fixed yet, check the order create
time or last update time as a cretira of checking entrance is not decided.
"""

import ConfigParser
import requests
import time
from alipay_trade import AlipayQueryTrade
from db import db_initialize
from schema import order
from urllib import urlencode

CONFIG_FILE = 'server.conf'

class OrderStatus():
    CREATED = 0
    WAIT_TO_PAY = 1
    PAYED = 2

def touch_order():
    ts = int(time.time())
    query = session.query(order).filter(order.orderid==orderid)
    query.update({order.last_check_time=ts})
    session.commit()
    
def mark_order_status(orderid, status):
    ts = int(time.time())
    query = session.query(order).filter(order.orderid==orderid)
    query.update({order.status=status,
                  order.last_check_time=ts})
    session.commit()
    
class AliQueryTradeRequest(object):
    def __init__(self, builder):
        cf = ConfigParser.ConfigParser()
        cf.read('trade.conf')
        self.alipay_server = cf.get('alipay_trade_common', 'server')
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
        self.builder = builder

    def send(self):
        sign = self.builder.get_signed_string()
        params_dict = self.builder.to_dict()
        params_dict['sign'] = sign
        encoded_url_params = urlencode(params_dict)
        encoded_post_data = urlencode(
            {'biz_content': self.builder.to_query_dict()}
            )
        url = self.alipay_server + "?" + encoded_url_params
        resp = self.curl(url, encoded_post_data)
        resp = json.loads(resp)
        if 'alipay_trade_query_response' not in resp:
            raise Exception(
                "fail to parse alipay response, no alipay_trade_query_response"
                "in the response message")
        return resp['alipay_trade_query_response']

    def curl(self, url, data):
        # all use the post http method
        r = requests.post(url, data=data, headers=self.headers)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        return r.text
        

def check_alipay_order(otn):
    qr_trade = AlipayQueryTrade()
    qr_trade.set_out_trade_no(otn)
    req = AliQueryTradeRequest(qr_trade)
    resp = req.send()
    if resp['trade_status'] == 'WAIT_BUYER_PAY':
        # do something
        pass
    else:
        pass # do someting
            


def check_wxpay_order():
    pass


def get_alipay_orders_to_check():
    """use yield to query one order once

    loop all the tuples, if there are a lot of tuples, this will take
    very long time. so there is a need to add limit param to the query
    statement, and also need to take care the script will always query
    the first serveral tuples, so that other tuples will be be accessed
    for a long time. currently just use the simplest way, since the fail
    to pay cases is not much a big amount.
    """
    from db import session
    query = session.query(order).filter(
        order.status==OrderStatus.WAIT_TO_PAY).filter(
        order.platform=='alipay')
    _tuples = query.all()
    for t in _tuples:
        print t.orderid, t.thirdpartyorderid
        check_alipay_order(t.orderid)


if __name__ == "__main__":
    cf = ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)
    db_initialize(cf)
    # firstly check the alipay orders, then wxpay orders
    get_alipay_orders_to_check()
