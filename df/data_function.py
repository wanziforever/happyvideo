#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os
import time
import logging
from statementdata import get_statement
from session import create_session

#from .exceptions import NoSupportDataType

#logger = logging.getLogger('data_function')

session = create_session()

def data_get(st_name, *args):
    mode = 'q'
    st = get_statement(st_name, mode)
    if not st:
        raise Exception( "data_get() cannot find the statment for %s " % st_name)

    s = "::".join(st.arguments)
    key = "%s::%s" %(st.id, s)

    st.build(*args)
    ret = st.process(session, mode)
    
    return ret
    
    
def data_insert(st_name, *args):
    mode = 'i'
    st = get_statement(st_name, mode)
    if not st:
        raise Exception( "data_insert() cannot find the statment for %s " % st_name)

    s = "::".join(st.arguments)
    key = "%s::%s" %(st.id, s)

    st.build(*args)
    ret = st.process(session, mode)
    return ret


def data_update(st_name, *args):
    mode = 'u'
    st = get_statement(st_name, mode)
    if not st:
        raise Exception( "data_update() cannot find the statment for %s " % st_name)

    s = "::".join(st.arguments)
    key = "%s::%s" %(st.id, s)

    st.build(*args)
    ret = st.process(session, mode)
    return ret
