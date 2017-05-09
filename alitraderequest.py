#!/usr/bin/env python

import json
import time
import ConfigParser
import requests
from urllib import urlencode, unquote
from alipay_trade import AlipayPreCreateTrade
from goods import Goods

class AliTradeRequest(object):
    def __init__(self, builder):
        cf = ConfigParser.ConfigParser()
        cf.read('trade.conf')
        self.alipay_server = cf.get('alipay_trade_common', 'server')
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
        self.builder = builder

    def send(self):
        print "in the base trade request send function"
        return "done"

    def curl(self, url, data):
        # all use the post http method
        r = requests.post(url, data=data, headers=self.headers)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        return r.text
            
class AliPreCreateTradeRequest(AliTradeRequest):
    def __init__(self, builder):
        AliTradeRequest.__init__(self, builder)

    def send(self):
        sign = self.builder.get_signed_string()
        params_dict = self.builder.to_dict()
        params_dict['sign'] = sign
        encoded_url_params = urlencode(params_dict)
        encoded_post_data = urlencode(
            {'biz_content': self.builder.order.to_dict()})
        
        url = self.alipay_server + "?" + encoded_url_params
        
        try:
            resp = self.curl(url, encoded_post_data)
        except Exception,e:
            raise Exception(str(e))

        resp = unquote(resp)
        try:
            resp = json.loads(resp)
        except Exception, e:
            raise Exception(
                "PreCreate request fail to jsonlize the response (%s):"
                % (str(e), resp[:40]))

        if 'alipay_trade_precreate_response' not in resp:
            raise Exception(
                "PreCreate request get invalid response, "
                "alipay_trade_precreate_response not found")
        return resp['alipay_trade_precreate_response']
            
