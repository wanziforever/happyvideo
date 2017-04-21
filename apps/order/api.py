#!/usr/bin/env python
#-*- coding: utf-8 -*-
from core import Application, make_app_wrappers, request
from df import data_function
from common.result import SuccResult, FailResult
from core.settings import settings

import logging
import json
import time

app = Application()
get, post = make_app_wrappers(app)
logger = logging.getLogger(__name__)
PREVIEW_URL = "/preview/api/auditlist"

@get('/sqltest')
def sqltest():
    print data_function.data_get("get_order_price", 1)
    return {"sql": "test"}


@get('/handlertest')
def handlertest():
    ret = data_function.data_get('get_order_copy_info', 1)
    return str(ret)


@get('/apply')
def create_order():
    params = request.params
    # get all the params
    domain = params.get('domainId', '')
    room = params.get('roomId', '')
    deviceid = params.get('deviceId', '')
    videoid = params.get('videoId', '')
    price = params.get('fee', 0)
    videoname = params.get('videoName', "")
    app_version_name = params.get('appVersionName', '')
    app_version_code = params.get('appVersionCode', '')
    platform = params.get('platform', '')
    
    clientinfo = ("appVersionName:%s, appVersionCode:%s"
                  % (app_version_name, app_version_code))

    if domain == '' or room == '' or deviceid == '' or \
           videoid == '' or platform == '':
        return FailResult(
            "domain, room, deviceid, video and platform should not "
            "be empty").export()
    
    _id = ""

    try:
        _id = data_function.data_insert(
            'ins_empty_order', domain, room, deviceid, clientinfo, price,
            videoid, videoname, platform)
    except Exception,e:
        return FailResult("fail to create order, %s" % str(e)).export()

    orderinfo = data_function.data_get('get_order_info_by_id', _id)
    if not orderinfo:
        return FailResult(
            "order created (%s) successfully, but cannot query it"
            % _id).export()
    
    if len(orderinfo) > 1:
        return FailResult(
            'order created (%s) successfully, but got more than 1'
            % _id).export()

    orderinfo = orderinfo[0]

    data = {
        'orderid': orderinfo.orderid,
        'domainId': orderinfo.lvl1_user,
        'roomId': orderinfo.lvl2_user,
        'deviceId': orderinfo.lvl3_user,
        'platform': orderinfo.platform,
        'videoId': orderinfo.resourceid,
        'videoName': orderinfo.resourceinfo,
        'platform': orderinfo.platform,
        'status': orderinfo.status
        }
    
    return SuccResult(data).export()


@get('/wechat_callback')
def wechat_callback():
    params = request.params
    orderid = params.get('orderid', '')
    #price = params.get('price', 0)
    #domainid = params.get('domainId', '')
    #roomid = params.get('roomId', '')
    #deviceid = params.get('deviceId', '')

    #if orderid == '' or domainid == '' or roomid = '' or deviceid == '':
    #    return FailResult(
    #        "domain, room, deviceid should not be empty").export()
    if orderid == '':
        return FailResult(
            "order id should be provided for confirm order"
            ).export()

    try:
        data_function.data_update('upd_order_confirm', 'confirm', 'wechat', orderid)
    except Exception,e :
        return FailResult(
            "fail to confirm order %s, for %s" % (orderid, str(e))
            ).export()
    #data_function.data_update('upd_order_confirm', 'confirm', 'wechat', orderid)
    
    return SuccResult().export()


@get('/alipay_callback')
def alipay_callback():
    params = request.params
    orderid = params.get('orderid', '')
    
    if orderid == '':
        return FailResult(
            "order id should be provided for confirm order"
            ).export()

    try:
        data_function.data_update('upd_order_confirm', 'confirm', 'alipay', orderid)
    except Exception,e :
        return FailResult(
            "fail to confirm order %s, for %s" % str(e)
            ).export()
    
    return SuccResult().export()


class AuthorizeMode(object):
    MODE1 = ('domainid', 'roomid', 'deviceid')
    MODE2 = ('domainid', 'roomid')
    
valid_interval = 48 * 60 * 60 #seconds
mode = 1 # reference to handler_valid_order_user::AUTH_MODE
@get('/authorize')
def authorize():
    params = request.params
    domainid = params.get('domainId', '')
    roomid = params.get('roomId', '')
    deviceid =  params.get('deviceId', '')
    videoid = params.get('videoId')

    if domainid == '' or roomid == '' or deviceid == '' or videoid == '':
        return FailResult(
            'domainId, roomId, deviceId, videoId should not be empty'
            ).export()

    ret = data_function.data_get("get_valid_order_for_user",
                                 domainid, roomid, deviceid, videoid,
                                 valid_interval, mode)
    if ret is None:
        return SuccResult([]).export()

    return SuccResult(ret).export()
        
