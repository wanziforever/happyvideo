#!/usr/bin/env python

import time

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, SmallInteger, BigInteger, func
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text, SmallInteger, Float, DateTime

def get_cur_time():
    return long(time.time())

class Base(object):
    @declared_attr
    def __tablename__( self ):
        return self.__name__
    __table_args__ = {'mysql_engine': 'InnoDB',
                     'mysql_charset': 'utf8'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(BigInteger, primary_key=True)
    customer_id = Column(BigInteger, nullable=True, default=1001, index=True)
    #version = Column(BigInteger, nullable=False, default=1)
    created_time = Column(Integer, nullable=False, default=get_cur_time)
    modified_time = Column(Integer, nullable=False, default=get_cur_time, onupdate=get_cur_time, index=True)

Base = declarative_base(cls=Base)
