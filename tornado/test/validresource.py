#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'domainId': '111',
    'roomId': '222',
    'deviceId': '333',
    'videoId': '444',
    }
api = "/order/validate"

cf = ConfigParser.ConfigParser()

def setup_url():
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    url = setup_url()
    print url
    print params
    r = requests.get(url, params)
    print r.text
    
    
