#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'orderId': '1112223331493304304422230000',
    }
api = "/order/query"

cf = ConfigParser.ConfigParser()

def setup_url():
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    url = setup_url()
    r = requests.get(url, params)
    print r.url
    print r.text
    
    
