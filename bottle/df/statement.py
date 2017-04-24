#!/usr/bin/env python

import importlib
import inspect
from datamodel.schema import all_tables
from handler.base_handler import DataHandler

class StatementType:
    SQL = 0
    HANDLER = 1

class Statement(object):
    def __init__(self, _id, _type=StatementType.SQL):
        self.type = _type
        self.id = _id
        self.arguments = []

    def build(self, *args):
        self.arguments = args

    def process(self, session):
        pass

class SQLStatement(Statement):
    def __init__(self, _id, sql):
        Statement.__init__(self, _id, StatementType.SQL)
        self.raw_sql = sql
        self.sql = ""
        self.replacement_num = 0

    def build(self, *args):
        print "statement.py::SQLStatement::build() going to build sql:", self.raw_sql
        self.replacement_num = self.raw_sql.count('?')
        print self.replacement_num, len(args), args
        if self.replacement_num != len(args):
            raise Exception("argument number is not right, %d need, but %d given"
                            % (self.replacement_num, len(args)))
        self.sql = self.raw_sql
        for arg in args:
            if isinstance(arg, int):
                self.sql = self.sql.replace('?', str(arg), 1)
            elif isinstance(arg, str):
                self.sql = self.sql.replace('?', "\'%s\'" % arg, 1)
        print "statement.py::SQLStatement::build() sql after build:", self.sql
        
    def process(self, session, mode):
        # run sql excutor
        return session.execute(self.sql).fetchall()

MODULE_CACHE = {}

class HandlerStatement(Statement):
    def __init__(self, _id, _class, *args):
        Statement.__init__(self, _id, StatementType.HANDLER)
        self._class_name = _class
        self._handler_class = None
        self.args = args
        self.filters = {}

    def build(self, *args):
        module_path = "df.handler." + self._class_name
        if module_path in MODULE_CACHE:
            self._handler_class = MODULE_CACHE[module_path]
        else:
            module = importlib.import_module(module_path)
            for m in dir(module):
                print "the module going to check is ", m
                m = getattr(module, m)
                if hasattr(m, "__handler__"):
                    self._handler_class = m
                    MODULE_CACHE[module_path] = m
                    break

        if not self._handler_class:
            print "cannot find module for ", self._class_name
            return
            
        if len(self.args) != len(args):
            raise Exception("argument number is not right, %d need, but %d given" % (len(self.args), len(args)))
        i = 0
        for arg in self.args:
            self.filters[arg] = args[i]
            i = i + 1
        
    def process(self, session, mode):
        if not self._handler_class:
            return
        
        if mode == 'q':
            ret = self._handler_class().process_query(session, **self.filters)
        elif mode == "i":
            ret = self._handler_class().process_insert(session, **self.filters)
        elif mode == 'u':
            ret = self._handler_class().process_update(session, **self.filters)
        else:
            print "invalid process mode", mode
        return ret


#class ORMStatement(Statement):
#    def __init__(self, _id, class_name, queries, conditions):
#        Statement.__init__(self, _id, StatementType.ORM)
#        self.tblname = class_name
#        self.query_fields = queries
#        self.cond_fields = conditions
#        self.filters = []
#        self._class = None
#
#    def build(self, *args):
#        self._class = all_tables[self.tblname]
#        if len(args) != len(self.cond_fields):
#            raise Exception("ORMStatement condition number and argument number not match (%d, %d)" % (len(args), len(self.cond_fields)))
#            
#        i = 0
#        for cond in self.cond_fields:
#            self.filters.append(getattr(self._class, cond) == args)
#            i = i + 1
#        print "--filters---", self.filters
#        
#    def process(self, session):
#        if len(self.cond_fields) > 0:
#            #return session.query(self._class).filter(**self.filters).all()
#            
#            return session.query(self._class).filter(self.filters).all()
#        else :
#            return session.query(self._class).all()
#
