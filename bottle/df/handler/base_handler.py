#!/usr/bin/env python
# -*- coding: utf-8 -*-  

from df.session import create_session
import logging
import inspect

logger = logging.getLogger('base_handler')


class DataHandler(object):
    def __init__(self):
        pass
    
    def process_query(self, session, **kwargs):
        pass

    def process_insert(self, session, **kwargs):
        pass

    def process_update(self, session, **kwargs):
        pass
    
