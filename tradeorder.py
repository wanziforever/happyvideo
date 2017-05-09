#!/usr/bin/env python
# encoding: utf-8

"""This module define the alipay and wxpay order definition, a order may
contain one or more goods information.
"""

import ConfigParser
import functools
from datetime import datetime, timedelta


class AliTradeOrder(object):
    """alipay order definition"""
    def __init__(self, tn, subject):
        self.trade_no = tn
        self.undiscountable_amount = ""
        self.total_amount = 0
        self.subject = subject
        self.body = ""
        self.seller_id = ""
        self.goodses = []
        self.operator_id = ""
        self.store_id = ""
        self.timeout_express = ""
        self.sys_service_provider_id = ""
        self.params_dict = {}
        self.initialize()

    def initialize(self):
        cf = ConfigParser.ConfigParser()
        cf.read("trade.conf")
        conf = functools.partial(cf.get, 'alipay_order')
        (self.store_id, self.operator_id, self.seller_id,
         self.sys_service_provider_id, self.timeout_express) = \
         (conf('store_id'), conf('operator_id'), conf('seller_id'),
          conf('sys_service_provider_id'), conf('timeout_express'))
        

    def check(self):
        if len(self.trade_no) == 0:
            raise Exception("the trade number should be provided")
        
    def add_goods(self, goods):
        """add a goods into the order, simply add the goods price together
        as the total price of the order.
        """
        self.goodses.append(goods)
        self.total_amount = self.total_amount + goods.get_total_price()

    def set_body(self, body):
        self.body = body

    def to_dict(self):
        return {
            'out_trade_no': self.trade_no,
            'undiscountable_amount': "0.01",
            'subject': self.subject,
            'body': self.body,
            'seller_id': self.seller_id,
            'extend_params': {"sys_service_provider_id": self.sys_service_provider_id},
            'store_id': self.store_id,
            'operator_id': self.operator_id,
            'total_amount': self.total_amount,
            'timeout_express': self.timeout_express,
            'goods_detail': [goods.to_dict() for goods in self.goodses]
            }

    def to_string(self):
        s = ("orderNo: %s, total: %d, subject: %s, goods(%d): ["
             %(self.trade_no, self.total_amount, self.subject, len(self.goodses)))
        
        for g in self.goodses:
            s += ("goodsId: %s, goodsName: %s, price: %s, quantity; %d" %
                  (g.goods_id, g.goods_name, g.price, g.quantity))
            
        s += "]"
        return s


class WXTradeOrder(object):
    """wxpay order data definition"""
    def __init__(self, tn, attach):
        self.trade_no = tn
        self.attach = attach
        self.body = ""
        # fee here should be a string type,
        # for there will be a len() on this field
        self.total_fee = "0" 
        self.time_start = ""
        self.time_expire = ""
        self.goods_tag = ""
        self.notify_url = ""
        self.trade_type = ""
        self.product_id = ""
        self.interval = 0
        self.initialize_from_conf()
        self.gen_timestamp()

    def initialize_from_conf(self):
        cf = ConfigParser.ConfigParser()
        cf.read('trade.conf')
        conf = functools.partial(cf.get, 'wxpay_order')
        (self.notify_url, self.interval, self.trade_type) = \
                          (conf('notify_url'), conf('interval'),
                           conf('trade_type'))

        self.interval = int(self.interval)

    def set_product_id(self, product_id):
        self.product_id = product_id

    def set_body(self, body):
        self.body = body

    def set_fee(self, fee):
        # should be a string type
        self.total_fee = str(fee)

    def set_goods_tag(self, tag):
        """only one goods information need to be set"""
        self.goods_tag = tag

    def gen_timestamp(self):
        """setup the order start time, and timeout time"""
        if self.interval < 60:
            raise Exception(
                "gen_timestamp for wxorder fail for little interval %d"
                % self.interval)
        ts = datetime.now()
        self.time_start = ts.strftime("%Y%m%d%H%M%S")
        ts = ts + timedelta(seconds=self.interval)
        self.time_expire = ts.strftime("%Y%m%d%H%M%S")

    def to_dict(self):
        return {
            'body': self.body,
            'attach': self.attach,
            'out_trade_no': self.trade_no,
            'total_fee' : self.total_fee,
            'goods_tag': self.goods_tag,
            'time_start': self.time_start,
            'time_expire': self.time_expire,
            'notify_url': self.notify_url,
            'trade_type': self.trade_type,
            'product_id': self.product_id
            }

    def to_string(self):
        s = ("orderNo: %s, total: %s, goods: %s"
             %(self.trade_no, self.total_fee, self.goods_tag,))
        
        return s
