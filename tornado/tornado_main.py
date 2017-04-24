#!/usr/bin/env python


import tornado.ioloop
import tornado.web

from orderhandler import (OrderApplyHandler,
                          OrderConfirmHandler,
                          ResourceValidationHandler)

application = tornado.web.Application([
    (r'/order/apply', OrderApplyHandler),
    (r'/order/confirm/(.+)_callback', OrderConfirmHandler),
    (r'/order/validate', ResourceValidationHandler)
    ])

if __name__ == "__main__":
    application.listen(8890)
    tornado.ioloop.IOLoop.instance().start()
