#!/usr/bin/env python

import logging
import os

def init_log(cf):
    logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=cf.get('server', 'logfile'),
                            filemode='w')


class MyLog(object):
    def __init__(self):
        self.open_traces = set()
        self.enable = False
        self.parse_trace_file()
        if len(self.open_traces) > 0:
            self.on()
            print "found open traces: ", ",".join([str(i) for i in self.open_traces])

    def parse_trace_file(self):
        p = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(p, 'tracefile'), 'r') as fd:
            for line in fd:
                for trace in line.split(','):
                    self.open_traces.add(int(trace.strip()))

        
    def open_traces(self, *traces):
        for t in traces:
            self.open_traces.add(t)

    def clear_traces(self):
        self.open_traces.clear()

    def on(self):
        self.enable = True

    def off(self):
        self.enable = False

    def trace(self, traceid, msg):
        if not self.enable:
            return
        
        if traceid not in self.open_traces:
            return
        
        logging.debug(msg)
        
mylog = MyLog()
debug = mylog.trace
turn_on_debug = mylog.on
