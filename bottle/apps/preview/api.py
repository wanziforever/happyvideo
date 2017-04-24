#!/usr/bin/env python
#-*- coding: utf-8 -*-
from core import Application, make_app_wrappers, request
from df import data_function
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
    #print "handlertest api result", str(data_function.data_get('get_order_copy_info', 1))
    ret = data_function.data_get('get_order_copy_info', 1)
    return str(ret)


