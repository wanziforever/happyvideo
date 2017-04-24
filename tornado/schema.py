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
    deleted = Column(SmallInteger, nullable=False, default=False, index=True)

Base = declarative_base(cls=Base)

class order(Base):
    orderid = Column(String(128), nullable=False, index=True)
    resourceid = Column(String(128), nullable=True)
    resourcetype = Column(SmallInteger, nullable=False)
    resourceinfo = Column(String(300), nullable=True)
    lvl1_user = Column(String(128), nullable=False)
    lvl2_user = Column(String(128), nullable=False)
    lvl3_user = Column(String(128), nullable=False)
    platform = Column(String(128), nullable=True)
    status = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    lastupdateinfo = Column(String(512), nullable=True)
    failreason = Column(String(256), nullable=True)
    failreasoncode = Column(SmallInteger, nullable=True)
    clientinfo = Column(String(512), nullable=True)
    history = Column(String(512), nullable=True)
    finishtime = Column(Integer, nullable=True)
