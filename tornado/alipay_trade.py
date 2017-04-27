#!/usr/bin/env python
# encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import base64
import ConfigParser
import functools
from datetime import datetime
from urllib import urlencode, quote_plus
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256, SHA
from Crypto.PublicKey import RSA

def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True, ensure_ascii=False)
    return sorted([(k, v) for k, v in data.items()])


def serialize_string(data):
    unsigned_items = ordered_data(data)
    unsigned_string = '&'.join("{}={}".format(k, v) \
                               for k, v in unsigned_items if len(v)!=0)
    return unsigned_string


def gensign(unsigned_string, private_key_file):
    key = RSA.importKey(open(private_key_file).read())
    #import textwrap
    #private_string = "-----BEGIN RSA PRIVATE KEY-----\n"
    #private_string += textwrap.fill(private_key, 64)
    #private_string += "\n-----END RSA PRIVATE KEY-----\n"
    #key = RSA.importKey(private_string)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
    sign = base64.b64encode(signature).decode("utf8")
    return sign


class AlipayTrade(object):
    def __init__(self, method, notify_url, return_url):
        self.app_id = ""
        self.version = ""
        self.sign_type = ""
        self.format = ""
        self.charset = "";
        self.alipay_sdk = ""
        # above data will be got from config file
        # following data will be set dynamicly
        self.notify_url = notify_url
        self.return_url = return_url
        self.timestamp = ""
        self.method = method
        self.params_dict = {}
        
        self.initialize_from_conf()

    def initialize_from_conf(self):
        cf = ConfigParser.ConfigParser()
        cf.read("trade.conf")
        conf = functools.partial(cf.get, 'alipay_trade_common')
        (self.app_id, self.version, self.sign_type, self.format, self.charset,
         self.alipay_sdk) = (conf('app_id'), conf('version'), conf('sign_type'),
                             conf('format'), conf('charset'), conf('alipay_sdk'))

    def gen_timestamp(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        self.gen_timestamp()
        return {
            'app_id': self.app_id,
            'version': self.version,
            'sign_type': self.sign_type,
            'format': self.format,
            'method': self.method,
            'alipay_sdk': self.alipay_sdk,
            'timestamp': self.timestamp,
            'notify_url': self.notify_url,
            'return_url': self.return_url,
            'charset': self.charset
            }

    def to_string(self):
        s = ("tradeInfo appid: %s, method: precreate, notify_url: %s, return_url: %s"
             % self.app_id, self.notify_url, self.return_url)
        return s


class AlipayPreCreateTrade(AlipayTrade):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read('trade.conf')
        AlipayTrade.__init__(self, 'alipay.trade.precreate',
                             cf.get('alipay_precreateTrade', 'notify_url'),
                             cf.get('alipay_precreateTrade', 'return_url'))
        self.private_key_file = cf.get('alipay_trade_common', 'private_key_file')
        
        self.biz_content = ""
        self.order = None

    def set_order(self, order):
        self.order = order

    def to_dict(self):
        # treat all the order content a string as a elemtn of the trade biz_content
        base = super(AlipayPreCreateTrade, self).to_dict()
        biz_content = json.dumps(self.order.to_dict(),
                                 ensure_ascii=False).replace(" ", "")
        base['biz_content'] = biz_content
        return base

    def get_serialize_string(self):
        return serialize_string(self.to_dict())

    def get_signed_string(self):
        return gensign(self.get_serialize_string(), self.private_key_file)

    def to_string(self):
        s = ("tradeInfo appid: %s, method: precreate, orderNo: %s, "
             "notify_url: %s, return_url: %s"
             % (self.app_id, self.order.trade_no, self.notify_url, self.return_url))
        return s
