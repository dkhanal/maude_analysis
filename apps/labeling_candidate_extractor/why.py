# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import sys
import os
import re
import logging
import datetime

def add_to_path(path):
    if path not in sys.path:
        print('Adding to sys.path: {}'.format(path))
        sys.path.append(path)
    else:
        print('Already in sys.path: {}'.format(path))

def initialize():
    base_path = os.path.dirname(__file__)
    add_to_path(os.path.abspath(os.path.join(base_path, '..', '..', 'shared')))
    add_to_path(os.path.abspath(os.path.join(base_path, 'lib')))

    global log_file_path
    log_file_path = os.path.join(base_path, 'out', 'why_session.log')

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)

    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'out')),
                           sharedlib.abspath(os.path.join(base_path, 'file_chunks'))])

def main(args=None):
    initialize()

    if args is None:
        args = sys.argv[1:]
    
    if len(args) == 0:
        logging.info('Usage python why.py <Report or Text Record Number> [return_on_first_find=True]')
        return

    output_dir = 'out'
    return_on_first_find = len(args) > 1 and not args[1].lower() in ['false']

    import sharedlib

    if not os.path.isabs(output_dir):
        output_dir = sharedlib.abspath(os.path.join(os.path.dirname(__file__), output_dir))

    match_count = 0
    for filename in os.listdir(output_dir):
        if filename.endswith('.process.txt'): 
            logging.info('Looking for {} in: {}...'.format(args[0], filename))
            with open(os.path.join(output_dir, filename), 'r') as f:
                for line in f:
                    match = re.search(args[0], line, re.IGNORECASE)
                    if match is not None:
                        logging.info('{}=> {}.'.format(filename, line))
                        match_count += 1
                        if return_on_first_find == True:
                            return
    if match_count == 0:
        logging.info('Nothing found for: {}.'.format(args[0]))

if __name__ == "__main__":
    main()
