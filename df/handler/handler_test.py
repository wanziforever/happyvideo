#!/usr/bin/env python

from base_handler import DataHandler
from ..datamodel.schema import order

class OrderTest(DataHandler):
    __handler__ = True
    def __init__(self):
        DataHandler.__init__(self)

    def process(self, session, **kwargs):
        orderid = kwargs['orderid']
        ret = session.query(order).filter(order.orderid==orderid).all()
        for i in ret:
            print i.orderid, i.info
        return ret
