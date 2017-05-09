#!/usr/bin/env python
# encoding: utf-8

"""The module define the wxpay trade system context, the class ``WXpayTrade``
hold the significant parameters for creating wxpay trade orders and signature.

wxpay has more than one type of trade, including pay, query, etc.
currently, we only support the pay in this module which is the service that
let user to scan qr to do charging work.

wxpay trade order only support one goods concept, and the only one description
field is needed to be put into the order.

wxpay support RSA and md5 signature method, and md5 is currently recommended.
it is much more easier from RSA. the process is just generate allmost the
same sorted parameter string, and a random string together, and call md5 to
generate a signature.

all the parameters will also put into the post http message body, and with the
XML format, exactly same value and parameter name with the params in the request.

qr information for wxpay is a picture url which is used to scan, so no need
for client to genrate a picture to scan.

"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import ConfigParser
import functools
import random
import hashlib
from datetime import datetime
from urllib import urlencode, quote_plus


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


def get_nonce_str(length=32):
    """generte a random string for a given length restriction"""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    str = ""
    for i in xrange(length):
        pos = random.randint(0, len(chars) - 1)
        str += chars[pos:pos+1]
    return str


def get_signed(unsigned_string):
    """use md5 function to generate a signature"""
    m = hashlib.md5()
    m.update(unsigned_string)
    return m.hexdigest().upper()


def toxml(data):
    """convert a json struct to a xml string"""
    xml = "<xml>"
    for k, v in data.items():
        if v.isdigit():
            xml += "<{key}>{value}</{key}>".format(key=k, value=v)
        else:
            xml += "<{key}><![CDATA[{value}]]></{key}>".format(key=k, value=v)

    xml += "</xml>"
    return xml


def xmlpost(url, xml):
    """send post http request with a xml content"""
    r = requests.post(url, data=xml)
    return r


class WXpayTrade(object):
    """wxpay trade data definition"""
    def __init__(self):
        self.app_id = ""
        self.key = ""
        self.mch_id = ""
        self.order = None
        self.sign = ""
        self.nonce_str = get_nonce_str()
        self.initialize_from_conf()

    def initialize_from_conf(self):
        cf = ConfigParser.ConfigParser()
        cf.read("trade.conf")
        conf = functools.partial(cf.get, 'wxpay_trade_common')
        (self.app_id, self.key, self.mch_id) = \
                      (conf('app_id'), conf('key'), conf('mch_id'))

    def set_order(self, order):
        self.order = order

    def to_string(self):
        s = ("tradeInfo appid: %s, mch_id: %s"
             % (self.app_id, self.mch_id))
        return s

    def to_dict(self):
        # do not provide the key and sign field in dict
        d = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': self.nonce_str
            }
        d.update(self.order.to_dict())
        return d

    def get_serialize_string(self):
        # as the wxpay requirement, the key field need to be put at the end
        return serialize_string(self.to_dict()) + "&key=%s" % self.key
        
    def get_signed_string(self):
        unsigned_string = self.get_serialize_string()
        self.sign = get_signed(unsigned_string)
        return self.sign
