import os
import logging

from core.settings import settings
from common.log import set_level, add_console_handler, add_file_handler

log_base_dir = '/home/postgres/log'

def init_log(mod, prefix):
    '''
    always keep ONE log file.
    '''
    log_file = os.path.join(log_base_dir, mod, '%s.log' % (prefix))
    log_level = settings.LOG_LEVEL.upper()
    le = logging.getLevelName(log_level)
    set_level(le)
    if settings.LOG_CONSOLE is True:
        add_console_handler(logging.DEBUG)
    add_file_handler(log_file, le, need_rotate=True)
    return


# Init the log with time rotating, under /var/log/vod/, level to ERROR 
def init_simple_log(prefix, level = logging.ERROR):
    logLevel = level
    log_file = os.path.join(log_base_dir, 'vod', '%s.log' % (prefix))
    add_file_handler(log_file, logLevel, need_rotate=True)

    #log_file = os.path.join(log_base_dir, 'vod', 'app.log')
    #add_file_handler(log_file, logLevel, need_rotate=True)
