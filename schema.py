#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, SmallInteger, BigInteger, func
from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Text, SmallInteger, Float, DateTime
from base import Base

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
    thirdpartyorderid = Column(String(128), nullable=True)
    waittopayinfo = Column(String(256), nullable=True)
    payinfo = Column(String(256), nullable=True)
    
