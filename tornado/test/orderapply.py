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
    'videoName': '外科风云',
    'platform': 'wechat',
    'appVersionCode': '34.346.34',
    'appVersionName': 'newdevelopedversion',
    'fee': '32'
    }
api = "/order/apply"

cf = ConfigParser.ConfigParser()


def setup_url():
    base = cf.get('target', 'url_base')
    return base + api

if __name__ == "__main__":
    cf.read('test.conf')
    url = setup_url()
    r = requests.get(url, params)
    print r.text
    
    
