# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import traceback
import logging

def initialize():
    logging.info('Registering unhandled exception handler...')
    sys.excepthook = log_exception

def log_exception(exception_type, exception_obj, traceback_info):
    logging.error(traceback.format_exception(exception_type, exception_obj, traceback_info))
    raise exception_obj