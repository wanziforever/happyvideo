#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
import six
from urllib import urlencode, quote_plus
from datetime import datetime
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256, SHA
from Crypto.PublicKey import RSA

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

alipay_url = "https://openapi.alipay.com/gateway.do"
#alipay_url = "http://47.90.6.240:8888/post/test"

app_id = '2017041806798698'
ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sign_type = 'RSA2'
#alipaySdkVersion = "alipay-sdk-php-20161101"
alipaySdkVersion = 'alipay-sdk-java-dynamicVersionNo'
notify_url = 'http://47.90.6.240:8888/order/confirm/alipay_callback'
return_url = 'http://47.90.6.240:8888/hello'
api_version = '1.0'

private_key_file = 'private_key.pem'

public_params = {
    'app_id': '2017041806798698',
    'method': 'alipay.trade.precreate',
    'version': api_version,
    'sign_type': 'RSA2',
    'format': 'json',
    'timestamp': '2017-04-27 14:14:19',
    'charset': 'UTF-8',
    'notify_url': 'http://47.90.6.240:8888/post/test',
    'return_url': 'http://47.90.6.240:8888/post/test',
    'alipay_sdk': 'alipay-sdk-java-dynamicVersionNo'
    }

post_data = {
    "out_trade_no":"1112223331493273659352220000",
    "undiscountable_amount":"0.01",
    "total_amount":120,
    "subject":"七龙珠全套，杀戮的游戏",
    "seller_id": "",
    "body":"共13卷，65本",
    "goods_detail":[
        {"goods_id":"324234","goods_name":"七龙珠全套，杀戮的游戏","quantity":1,"price":120},
        ],
    "operator_id":"test_operator_id",
    "store_id":"test_store_id",
    "extend_params":{"sys_service_provider_id":"2088100200300400500"},
    "timeout_express":"5m",
    }


def post(url, data):
    headers = {'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    newdata = {}
    newdata['biz_content'] = data
    encodestring = urlencode(newdata)
    print "encode post data :", encodestring
    #for k, v in data.items():
    #    encodedata[k] = urlencode(v)
    return requests.post(url, data=encodestring, headers=headers)


def build_biz_content(data):
    s = json.dumps(data)
    return s


def sort_params(public_params):
    pass

def build_signstring(params, data):
    new = {}
    for k, v in params.items():
        new[k] = v
    for k, v in data.items():
        new[k] = v
    return new


def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        #data[key] = json.dumps(data[key], sort_keys=True, ensure_ascii=False).replace(" ", "")
        data[key] = json.dumps(data[key], sort_keys=True, ensure_ascii=False)#.replace(" ", "")
    return sorted([(k, v) for k, v in data.items()])

def loop_jsonlize(s):
    d = {}
    try:
        d = json.loads()
        for k, v in d.items():
            pass
    except Exception, e :
        pass
        
        
def encode_dict(params):
    return {k: six.u(v).encode('utf-8')
            if isinstance(v, str) else v.encode('utf-8')
            if isinstance(v, six.string_types) else v
            for k, v in six.iteritems(params)}

def getSignContent(data):
    unsigned_items = ordered_data(data)
    l = []
    #for k, v in unsigned_items:
    #    if len(v) == 0:
    #        print "invalid length for ", k
    #        continue
    #    l.append("{}=\"{}\"".format(k, v))
    #unsigned_string = '&'.join(l)
    unsigned_string = '&'.join("{}={}".format(k, v) for k, v in unsigned_items if len(v)!=0)
    return unsigned_string


def gensign(unsigned_string):
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
    

if __name__ == "__main__":
    print
    print
    print

    data = {}
    for k, v in public_params.items():
        data[k] = v


    #data['biz_content'] = json.dumps(post_data, ensure_ascii=False)
    biz_content = json.dumps(post_data, ensure_ascii=False).replace(" ", "")
    data['biz_content'] = biz_content

    unsigned_string = getSignContent(data)
    
    print unsigned_string

    sign = gensign(unsigned_string)
    print
    print "----------------signature------------------"
    print sign

    data['sign'] = sign
    #data['sign_type'] = 'RSA2'
    
    alipay_url = "https://openapi.alipay.com/gateway.do"
    final_url = alipay_url + "?"
    
    final_url += urlencode(data)
    #for k, v in data.items():
    #    final_url += "{}={}&".format(k, quote_plus(v))
    #final_url = final_url[:-1]
    
    #r = requests.post(final_url, data=post_data)
    r = post(final_url, post_data)
    
    print
    print "========================request response===================="
    print r.text
