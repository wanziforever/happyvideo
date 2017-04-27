#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'orderid': '1112223331492761236905280000'
    }
data = {
    'postorderid': '1112223331492761236905280000'
    }
api = "/post/test"

cf = ConfigParser.ConfigParser()

def setup_url():
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    url = setup_url()
    print url
    r = requests.post(url, params=params, data=data)
    print r.text
    
