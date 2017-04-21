#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
time related utility
@author: Guojian Shao
"""
import datetime
import time
from common.errors import BadArgValueError


def strpmills(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.datetime.strptime(datetime_str, format)
    return long(time.mktime(dt.timetuple()))

def get_today_yesterday():
    now = time.gmtime()
    today = datetime.datetime(now[0], now[1], now[2])
    yesterday = today - datetime.timedelta(days=1)
    return today, yesterday

def now_seconds():
    return long(time.mktime(datetime.datetime.now().timetuple()))

def strpBJTime(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    if not datetime_str:
        return None
    dt = datetime.datetime.strptime(datetime_str, format)
    gmtdt = dt - datetime.timedelta(hours=8)
    return long(time.mktime(gmtdt.timetuple()))
    
def toBJTimeStr(seconds):
    if not seconds:
        return None
    bjst = datetime.datetime.utcfromtimestamp(float(seconds)) + datetime.timedelta(hours=8)
    return bjst.strftime("%Y-%m-%d %H:%M:%S")

def toBJTimeOtherStr(seconds):
    bjst = datetime.datetime.utcfromtimestamp(float(seconds)) + datetime.timedelta(hours=8)
    return bjst.strftime("%Y.%m.%d")

def toUtcTimeStr(seconds):
    if not seconds:
        return None
    bjst = datetime.datetime.utcfromtimestamp(float(seconds))
    return bjst.strftime("%Y-%m-%d %H:%M:%S")

def str_to_timstamp(time_str):
    return long(time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))) - (8 * 60 * 60 + time.timezone)

def utcToBJFormat(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    if not datetime_str:
        return None
    dt = datetime.datetime.strptime(datetime_str, format)	
    bjdt = dt + datetime.timedelta(hours=8)
    bjstr = bjdt.strftime("%Y-%m-%d %H:%M:%S")
    return bjstr

def bjToUtcFormat(datetime_str, format='%Y-%m-%d %H:%M:%S'):
    if not datetime_str:
        return None
    dt = datetime.datetime.strptime(datetime_str, format)	
    utcdt = dt - datetime.timedelta(hours=8)
    utcstr = utcdt.strftime("%Y-%m-%d %H:%M:%S")
    return utcstr

def get_cur_time():
    return long(time.time())

if __name__ == "__main__":
     #print bjToUtcFormat("2015-06-22 14:42:39")
     print toUtcTimeStr(1450393200)
