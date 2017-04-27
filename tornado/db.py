#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

DB = 'mysql'
#DBNAME = 'happyvideo'

session = None

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

def create_db_session(host, user, pwd, dbname, verbose):
    conn_str = '{db}://{user}:{pwd}@{host}/{dbname}?charset=utf8'.format(
        db=DB, user=user, pwd=pwd, host=host, dbname=dbname)
    engine = create_engine(conn_str, pool_recycle=3600, echo_pool=False, echo=verbose)
    session_class = scoped_session(sessionmaker(engine, autoflush=False))
    return session_class()

def db_initialize(conf):
    global session
    if session is not None:
        print "db session is already startup"
        return
    host = conf.get('db', 'host')
    db = conf.get('db', 'db')
    verbose = conf.get('db', 'verbose')
    if verbose.lower() in ['1', 'true']:
        verbose = True
    else:
        verbose = False
    user = conf.get('db', 'user')
    pwd = conf.get('db', 'password')
    session = create_db_session(host, user, pwd, db, verbose)
