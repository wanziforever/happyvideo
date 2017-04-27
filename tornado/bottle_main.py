#!/usr/bin/env python

import ConfigParser
import functools
import json
from bottle import route, run
from session import create_db_session
from schema import order

DBNAME = 'happyvideo'
cf = ConfigParser.ConfigParser()
cf.read('app.conf')

dbconf = functools.partial(cf.get, 'db')
dbhost, dbuser, dbpwd = \
        dbconf('host'), dbconf('user'), dbconf('password')
session = create_db_session(dbhost, dbuser, dbpwd)

@route('/order/api/apply')
def order_apply():
    params = request.params
    _tuple = session.query(order).filter(order.id==1).one()
    print _tuple.orderid


@route('/order/api/authorize')
def order_authroize():
    params = request.params
    




if __name__ == "__main__":
    run(host='0.0.0.0', port=8088, debug=True)
