#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import ConfigParser

params = {
    'domainId': '111',
    'roomId': '222',
    'deviceId': '333',
    'videoId': '3434535',
    }
api = "/order/validate"

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
    
    
