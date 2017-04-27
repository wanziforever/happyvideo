#!/usr/bin/env python

import ConfigParser
import functools

class TradeOrder(object):
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
