#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

DB = 'mysql'
DBNAME = 'happyvideo'

class _Session(Session):
    def __init__(self, *args, **kwargs):
        super(_Session, self).__init__(*args, **kwargs)

    def flush(self, objects=None):
        for entity in self.dirty:
            now = long(time.time())
            if hasattr(entity, 'modified_time'):
                entity.modified_time = now
            if hasattr(entity, 'version'):
                if entity.version is None:
                    entity.version = 1
                else:
                    entity.version += 1
        for entity in self.new:
            now = long(time.time())
            if hasattr(entity, 'created_time'):
                entity.created_time = now
            if hasattr(entity, 'modified_time'):
                entity.modified_time = now
            if hasattr(entity, 'version'):
                entity.version = 1
        super(_Session, self).flush(objects)

def create_db_session(host, user, pwd):
    conn_str = '{db}://{user}:{pwd}@{host}/{dbname}?charset=utf8'.format(
        db=DB, user=user, pwd=pwd, host=host, dbname=DBNAME)
    engine = create_engine(conn_str, pool_recycle=3600, echo_pool=False, echo=True)
    session_class = scoped_session(sessionmaker(engine, autoflush=False))
    return session_class()
