# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import logging

# Logging related
def initialize(log_file_abs_path):
    logger = logging.getLogger()
    logger.handlers = [] # Clears any handlers previously, implicitly,p registered.

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - [%(threadName)s] - [%(levelname)s] - %(message)s")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)

    logger.addHandler(consoleHandler)

    log_dir = os.path.dirname(log_file_abs_path)

    if not os.path.exists(log_dir):
        logging.info('Creating directory for logs: {}'.format(log_dir))
        os.makedirs(log_dir)

    fileHandler =  logging.FileHandler(log_file_abs_path)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logging.info('Log file for this session: {}.'.format(log_file_abs_path))

def close_logger():
    logging.info('Shutting down logger...')
    logging.shutdown()