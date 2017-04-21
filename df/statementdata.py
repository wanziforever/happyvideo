#!/usr/bin/env python

from statement import SQLStatement, HandlerStatement

def get_statement(name, mode):
    if name in SQL_STATEMENTS:
        return SQL_STATEMENTS[name]

    if name in HANDLER_STATEMENTS:
        return HANDLER_STATEMENTS[name]

    return None


# the id for sql statement start from 1000
SQL_STATEMENTS = {
    "get_order_info_by_id" : SQLStatement(1000, "select orderid, lvl1_user, lvl2_user, "
                                          "lvl3_user, platform, resourceid, resourcetype, "
                                          "resourceinfo, status from `order` where orderid=?"),
    }

# the id for handler statement start from 4000
HANDLER_STATEMENTS = {
    "get_test" : HandlerStatement(4000, "handler_test", ("orderid")),
    "ins_empty_order" : HandlerStatement(4001, "handler_order_create", 'lvl1_user',
                                         'lvl2_user', 'lvl3_user', 'clientinfo', 'price',
                                         'resourceid', 'resourceinfo', 'platform'),
    #"get_order_info" : HandlerStatement(4002, "handler_order_get", 'orderid')
    "get_valid_order_for_user" : HandlerStatement(4002, "handler_valid_order_user",
                                                  'lvl1_user', 'lvl2_user', 'lvl3_user', 'resourceid', 'interval', 'mode'),
    "upd_order_confirm" : HandlerStatement(4003, "handler_order_update", 'mode', 'platform', 'orderid')
    }
