#!/usr/bin/env python
# encoding: utf-8

"""main routine to define the access api and handler mapping under the
tornado framework. start the tornado IO Loop.
"""

import tornado.ioloop
import tornado.web
import ConfigParser
import tornado
import json
import sys

from db import db_initialize
from log import init_log

cf = ConfigParser.ConfigParser()
CONFIG_FILE = 'server.conf'
cf.read(CONFIG_FILE)
port = cf.get('server', 'port')


def display_important_conf(cf):
    """show some significant configuration parameters"""
    print "server port: %s" % port
    print "database host: %s" % cf.get('db', 'db')
    print "logfile: %s" % cf.get('server', 'logfile')


class HellowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hellow World!!')


class TestHandler(tornado.web.RequestHandler):
    def post(self):
        print "request url : ", self.request.uri
        print "request.body", self.request.body
        #print tornado.escape.json_decode(self.request.body)
        print "request.body_argument", str(self.request.body_arguments)
        print "----------------"
        print json.dumps({k: self.get_argument(k) for k in self.request.arguments})
        self.write('success')
        #self.write(json.dumps({k: self.get_argument(k) for k in self.request.arguments}))

    def get(self):
        print "request url:", self.request.uri
    

if __name__ == "__main__":

    cf.read(CONFIG_FILE)

    init_log(cf)
    db_initialize(cf)
    if len(sys.argv) > 1:
        port = sys.argv[1]

    display_important_conf(cf)

    from orderhandler import (OrderApplyHandler,
                              OrderConfirmHandler,
                              ResourceValidationHandler,
                              OrderQueryHandler)
    
    application = tornado.web.Application([
        (r'/order/apply', OrderApplyHandler),
        (r'/order/confirm/(.+)_callback', OrderConfirmHandler),
        (r'/order/query', OrderQueryHandler),
        (r'/order/validate', ResourceValidationHandler),
        (r'/hello', HellowHandler)
        ])
    
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
