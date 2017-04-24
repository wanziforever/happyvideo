#!/usr/bin/env python

# success result
class SuccResult(object):
    def __init__(self, data=None, msg=''):
        self.succ_msg = msg
        self.data = []
        if data is None:
            return
        if isinstance(data, list):
            for l in data:
                self.data.append(l)
        else:
            self.data.append(data)

    def set_data(self, data):
        if not data:
            self.data.append(data)

    def clear_data(self):
        self.data = []

    def export(self):
        return {'result': 'succeed',
                'data': self.data,
                'msg': self.succ_msg}

# fail result
class FailResult(object):
    def __init__(self, msg):
        self.failed_msg = msg

    def set_fail_msg(self, msg):
        self.failed_msg = msg

    def export(self):
        return {'result': 'failed',
                'msg': self.failed_msg}
