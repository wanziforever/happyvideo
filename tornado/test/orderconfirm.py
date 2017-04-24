#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'orderid': '1112223331492761236905280000'
    }
api = "/order/confirm/wechat_callback"
#api = "/order/confirm/waadfads_callback"
api = "/order/confirm/alipay_callback"

cf = ConfigParser.ConfigParser()

def setup_url():
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    url = setup_url()
    r = requests.get(url, params)
    print r.text
    
