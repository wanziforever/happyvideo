#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'orderid': '1112223331492761236905280000'
    }
wxapi = "/order/confirm/wxpay_callback"
#api = "/order/confirm/waadfads_callback"
aliapi = "/order/confirm/alipay_callback"

cf = ConfigParser.ConfigParser()

alipay_response_data = {
    'open_id': "132434345",
    'trade_no': "alipay_trade_32345",
    'seller_id': '12234',
    'buyer_id': '4534',
    'buyer_logon_id': '123****435',
    'out_trade_no': "1013101HaierKTU84Pb0a37e57b47c1493365792542540000",
    #'trade_status': 'WAIT_BUYER_PAY'
    'trade_status': 'PAYED'
    }

wxpay_response_data = '''<xml><appid><![CDATA[wx426b3015555a46be]]></appid>
<attach><![CDATA[外科风云]]></attach>
<bank_type><![CDATA[CFT]]></bank_type>
<cash_fee><![CDATA[1]]></cash_fee>
<fee_type><![CDATA[CNY]]></fee_type>
<is_subscribe><![CDATA[N]]></is_subscribe>
<mch_id><![CDATA[1900009851]]></mch_id>
<nonce_str><![CDATA[wlbzfif21s9f2stervdse81749qt159j]]></nonce_str>
<openid><![CDATA[oHZx6uN8B0j8NRt1egXkJYj-444A]]></openid>
<out_trade_no><![CDATA[1112223331493431379451220000]]></out_trade_no>
<result_code><![CDATA[SUCCESS]]></result_code>
<return_code><![CDATA[SUCCESS]]></return_code>
<sign><![CDATA[31F19F702DA308BC774AAB9AE2A12A8B]]></sign>
<time_end><![CDATA[20170429100326]]></time_end>
<total_fee>1</total_fee>
<trade_type><![CDATA[NATIVE]]></trade_type>
<transaction_id><![CDATA[4004092001201704298760300458]]></transaction_id>
</xml>'''

def send_alipay_response():
    url = setup_url(alipay)
    return requests.post(url, data=alipay_response_data)

def send_wxpay_response():
    url = setup_url(wxapi)
    return requests.post(url, data=wxpay_response_data)


def setup_url(api):
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    #url = setup_url(wxapi)
    url = setup_url(aliapi)
    print url
    #r = send_alipay_response()
    r = send_wxpay_response()
    print r.content

