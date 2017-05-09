#!/usr/bin/env python
# encoding: utf-8

import requests
import base64
import json
from datetime import datetime
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
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

private_key_file = 'rsa_private_key.pem'

public_params = {
    'app_id': app_id,
    'method': 'alipay.trade.precreate',
    'version': api_version,
    'format': 'json',
    'timestamp': ts,
    'charset': 'utf-8',
    #'notify_url': notify_url,
    #'return_url': return_url,
    'alipay_sdk': alipaySdkVersion,
    }

post_data = {
    "out_trade_no":"qrpay20160826053813582",
    "total_amount":"0.01",
    "timeout_express":"5m",
    "subject":"方倍工作室-支付宝-当面付-扫码支付"
    }


def build_biz_content(data):
    s = json.dumps(data)
    return s



def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True).replace(" ", "")
    return sorted([(k, v) for k, v in data.items()])


def getSignContent(data):
    unsigned_items = ordered_data(data)
    l = []
    for k, v in unsigned_items:
        if len(v) == 0:
            print "invalid length for ", k
            continue
        l.append("{}=\"{}\"".format(k, v))
    unsigned_string = '&'.join(l)
    #unsigned_string = '&'.join("{}={}".format(k, v) for k, v in unsigned_items if len(v)!=0)
    return unsigned_string


def gensign(unsigned_string):
    key = RSA.importKey(open(private_key_file).read())
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
    sign = base64.b64encode(signature).decode("utf8").replace("\n", "")
    return sign
    

if __name__ == "__main__":

    data = {}
    for k, v in public_params.items():
        data[k] = v

    for k, v in post_data.items():
        data[k] = v
    
    unsigned_string = getSignContent(data)
    
    print unsigned_string
    sign = gensign(unsigned_string)
    public_params['sign'] = sign
    public_params['sign_type'] = "RSA2"
    public_params['biz_content'] = json.dumps(post_data)
    print
    print "public_params->", public_params
    print
    print "post_data->", post_data
    #r = requests.get(url=alipay_url, params=public_params)
    r = requests.post(url=alipay_url, params=public_params, data=post_data)
    print "-----------------------------------------------------"
    print r.text
    print
