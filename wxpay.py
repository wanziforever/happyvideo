#!/usr/bin/env python
# encoding: utf-8

import time
import random
import requests
from urllib import urlencode, quote_plus
import hashlib
from datetime import datetime, timedelta
import xmltodict

appid = 'wx426b3015555a46be'
mchid = '1900009851'
key = '8934e7d15453e97507ef794cf7b0519d'
appsecret = '7813490da6f1265e4901ffb80afaa36f'

sslcert_file = 'apiclient_cert.pem'
sslkey_file = 'apiclient_key.pem'

product_id = '123456789'
wxpay_url = 'weixin://wxpay/bizpayur'

test_data = {
    'appid': appid,
    'mch_id': mchid,
    'key': key,
    'appsecret': appsecret
    }

delta = 600
start_time = datetime.now()
end_time = start_time + timedelta(seconds=delta)

order_data = {
    'body': '外科风云',
    'attach': '外科风云',
    'out_trade_no': '1112223331493428620961210000',
    'total_fee': "1", # should be a string type, for len() on this field
    #'time_start':start_time.strftime("%Y%m%d%H%M%S"),
    #time_expire':end_time.strftime("%Y%m%d%H%M%S"),
    'time_start': str(20170429091701),
    'time_expire': str(20170429092701),
    'goods_tag':'外科风云',
    'notify_url': 'http://47.90.6.240:8888/order/confirm/wxpay_callback',
    'trade_type': 'NATIVE',
    'product_id': '3434535',
    }

def set_order():
    result = {}
    result.update(test_data)
    result.update(order_data)
    result.pop('appsecret')
    result.pop('key')
    return result
    

def get_nonce_str(length=32):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    str = ""
    for i in xrange(length):
        pos = random.randint(0, len(chars) - 1)
        str += chars[pos:pos+1]

    str = "h0hwoj7jn8eekkuca1fx4y11o2trufrd"
    return str

def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True, ensure_ascii=False)
    return sorted([(k, v) for k, v in data.items()])

def getSignContent(data):
    unsigned_items = ordered_data(data)
    unsigned_string = '&'.join("{}={}".format(k, v) for k, v in unsigned_items if len(v)!=0)
    return unsigned_string

def get_signed(data):
    unsigned_string = getSignContent(data)
    unsigned_string += "&key=%s" % key
    print "unsigned_string: ", unsigned_string
    m = hashlib.md5()
    m.update(unsigned_string)
    return m.hexdigest().upper()

def toxml(data):
    #newdata = sorted([(k, v) for k, v in data.items()])
    xml = "<xml>"
    for k, v in data.items():
        if v.isdigit():
            xml += "<{key}>{value}</{key}>".format(key=k, value=v)
        else:
            xml += "<{key}><![CDATA[{value}]]></{key}>".format(key=k, value=v)

    xml += "</xml>"
    return xml

def xmlpost(url, xml):
    r = requests.post(url, data=xml)
    return r

def get_prepay_url(product_id):
    test_data['product_id'] = product_id
    test_data['nonce_str'] = get_nonce_str()
    signed = get_signed(test_data)
    test_data['sign'] = signed
    return '&'.join("{}={}".format(k, v) for k, v in test_data.items())

def get_pay_url():
    result = set_order()
    result['nonce_str'] = get_nonce_str()
    #result['spbill_create_ip'] = '192.168.0.1'
    signed = get_signed(result)
    result['sign'] = signed
    xml = toxml(result)
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    print "url:", url
    print "xml:",xml
    return xmlpost(url, xml)
    
if __name__ == "__main__":
    #url = get_prepay_url(product_id)
    #url = wxpay_url + "?" + url
    #final_url = "http://paysdk.weixin.qq.com/example/qrcode.php?data=" + quote_plus(url)
    #print final_url
    r = get_pay_url()
    print "response:"
    print r.content
    print
    print
    j = xmltodict.parse(r.text)
    print j
    url = j['xml']['code_url']
    final_url = "http://paysdk.weixin.qq.com/example/qrcode.php?data=" + quote_plus(url)
    print final_url
    
    
