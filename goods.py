#!/usr/bin/env python
# encoding: utf-8

"""This goods definition currently is only for alipay context"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Goods(object):
    def __init__(self, _id, name, amount, price):
        self.goods_id = _id
        self.goods_name = name
        self.quantity = amount
        if isinstance(price, str) and not price.isdigit():
            raise Exception('goods price should a number, but currently is %s' % price)
        self.price = int(price)
        self.price = self.price / 100.0
            
        self.check()

    def check(self):
        if not isinstance(self.quantity, int):
            raise Exception("goods quantity should be a integer type")
        if not isinstance(self.price, float):
            raise Exception("goods price should be a integer type")

    def set_body(self, body):
        self.body = body
        
    def to_dict(self):
        return {
            'goods_id': self.goods_id,
            'goods_name': self.goods_name,
            'quantity': self.quantity,
            'price': self.price
            }
        
    def get_total_price(self):
        return self.price * self.quantity
