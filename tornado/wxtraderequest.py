#!/usr/bin/env python
# encoding: utf-8

import json
import time
import ConfigParser
import requests
import xmltodict
from urllib import urlencode, unquote


def toxml(data):
    xml = "<xml>"
    for k, v in data.items():
        if v.isdigit():
            xml += "<{key}>{value}</{key}>".format(key=k, value=v)
        else:
            xml += "<{key}><![CDATA[{value}]]></{key}>".format(key=k, value=v)

    xml += "</xml>"
    return xml

class WXTradeRequest(object):
    def __init__(self, builder):
        cf = ConfigParser.ConfigParser()
        cf.read('trade.conf')
        self.wxpay_server = cf.get('wxpay_trade_common', 'server')
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
            }
        self.builder = builder

    def send(self):
        print "in the base trade request send function"
        return "done"

    def curl(self, data):
        # all use the post http method
        r = requests.post(
            self.wxpay_server, data=data, headers=self.headers)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        return r.text
            
class WXTradePayRequest(WXTradeRequest):
    def __init__(self, builder):
        WXTradeRequest.__init__(self, builder)

    def send(self):
        data = self.builder.to_dict()
        data['sign'] = self.builder.get_signed_string()
        print "sign:", data['sign']
        xml = toxml(data)
        print "xml:", xml
        try:
            resp = self.curl(xml)
        except Exception,e:
            raise Exception(str(e))

        resp = unquote(resp)

        print "resp:", resp
        
        try:
            resp = xmltodict.parse(resp)
        except Exception, e:
            raise Exception(
                "WXTradePay request fail to jsonlize the response (%s):"
                % (str(e), resp[:40]))

        if 'xml' not in resp:
            raise Exception(
                "wxpay qr request get invalid response, "
                "xml tag not found, %s" % json.dumps(resp))
        return resp['xml']
            
