#!/usr/bin/env python
# encoding: utf-8

"""The module define the alipay trade system context, the class ``AlipayTrade``
hold some significant parameters for creating aliy trade orders and signature.

Alipay trade has more than one trade type, like the pay, query, precreate, etc.
we currenty only support precreate interface with the service that leting user
scan the qr, and charging it in the phone.

Alipay system make a trade containing multiple goods, every goods has its own
price and quantity, and the total price can be different from the prices with
all the goods plused together, because it allow to make some discount rate.
but anyway, happyvideo currently only have one goods in a trade order, and no
discount provided. the goods subject is just as the order description.

for sercurity reason, alipay need a signature for all its request, and provide
a signature generating mechanism, like this:
put all the parameters in a sorted string like params1=value1&params2=value2,
and use RSA2(a SHA356 algorithm) to make a signature, one notification is the
biz_content parameter, it is the json.dumps version of all the merchant json
data.

for the post message body, it should content exactly the same data in the
``biz_contebt`` parameter in the request.

the qr inforamtion returned from alipay is a charging url, and when the client
recieve the qr url, it should be use tool to generate a picture for smart
phone to have a scan.

"""

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
    """put the topest level of keys ordered to a kv list"""
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True, ensure_ascii=False)
    return sorted([(k, v) for k, v in data.items()])


def serialize_string(data):
    """put the ordered kv list into a & serperated string"""
    unsigned_items = ordered_data(data)
    unsigned_string = '&'.join("{}={}".format(k, v) \
                               for k, v in unsigned_items if len(v)!=0)
    return unsigned_string


def gensign(unsigned_string, private_key_file):
    """use the RSA2 function to generate a signature"""
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
    """alipay trade data definitions, some significant data are from
    configuration file.
    """
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
        self.initialize_from_conf()
        self.gen_timestamp()

    def initialize_from_conf(self):
        """read config data from config file."""
        cf = ConfigParser.ConfigParser()
        cf.read("trade.conf")
        conf = functools.partial(cf.get, 'alipay_trade_common')
        (self.app_id, self.version, self.sign_type, self.format, self.charset,
         self.alipay_sdk) = (conf('app_id'), conf('version'), conf('sign_type'),
                             conf('format'), conf('charset'), conf('alipay_sdk'))
        self.private_key_file = cf.get('alipay_trade_common',
                                       'private_key_file')

    def gen_timestamp(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """export all the base trade data into a dictionary."""
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
        
        self.biz_content = ""
        self.order = None

    def set_order(self, order):
        self.order = order

    def to_dict(self):
        """beside the base class to_dict() function, also add the order data
        into the biz_content.
        """
        # treat all the order content a string as a elemtn of the trade biz_content
        base = super(AlipayPreCreateTrade, self).to_dict()
        biz_content = json.dumps(self.order.to_dict(),
                                 ensure_ascii=False).replace(" ", "")
        base['biz_content'] = biz_content
        return base

    def get_serialize_string(self):
        """get the serialized string for all its parameters."""
        return serialize_string(self.to_dict())

    def get_signed_string(self):
        """return the signatures."""
        return gensign(self.get_serialize_string(), self.private_key_file)

    def to_string(self):
        """return string to show the trade information."""
        s = ("tradeInfo appid: %s, method: precreate, orderNo: %s, "
             "notify_url: %s, return_url: %s"
             % (self.app_id, self.order.trade_no, self.notify_url, self.return_url))
        return s


class AlipayQueryTrade(AlipayTrade):
    """query trade order is simple, there is no goods concent, so just create
    a new class with inherit from AlipayTrade class.
    query request can either contain the tradeNo or outTradeNo.
    """
    def __init__(self):
        self.out_trace_no = ""
        self.trade_no = ""
        AlipayTrade.__init__(self, 'alipay.trade.query',"", "")
        
    def set_trade_no(self, tn):
        self.trade_no = tn

    def set_out_trade_no(self, otn):
        self.out_trade_no = otn

    def get_trade_no(self):
        return self.trade_no

    def get_out_trade_no(self):
        return self.out_trade_no

    def biz_content(self):
        return json.dumps({'out_trade_no':self.out_trade_no,
                           'trade_no':self.trade_no})

    def to_query_dict(self):
        return {'out_trade_no': self.out_trade_no,
                'trade_no': self.trade_no}
    
    def to_dict(self):
        base = super(AlipayQueryTrade, self).to_dict()
        biz_content = json.dumps(self.to_query_dict(),
                                 ensure_ascii=False).replace(" ", "")
        base['biz_content'] = biz_content
        return base

    def get_signed_string(self):
        return gensign(self.get_serialize_string(), self.private_key_file)

    def get_serialize_string(self):
        return serialize_string(self.to_dict())

        
    
