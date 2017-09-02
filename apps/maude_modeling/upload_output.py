# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import sys
import os
import datetime
import logging

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
    log_file_path = os.path.join(base_path, 'out', 'modeling_upload_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")))

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)
    
def main(args=None):
    initialize()

    logging.info('-- Uploader -- ')
    logging.info('Usage python upload.py [all]')
    if args is None:
        args = sys.argv[1:]

    output_dir = 'out'
    all = len(args) > 1 and args[1].lower() in 'all'

    import config
    import sharedlib

    output_dir = sharedlib.abspath(config.output_dir)

    files_in_output_dir = os.listdir(output_dir)

    files_to_upload = [os.path.join(output_dir, f) for f in files_in_output_dir if f.lower().endswith('.zip')]

    logging.info(files_to_upload)
    logging.info('Upload these files? [y/n] ')
    upload_confirmation = sharedlib.get_char_input()
    if not isinstance(upload_confirmation, str):
        upload_confirmation = bytes.decode(upload_confirmation)
    if upload_confirmation == 'y':
        sharedlib.upload_files_to_labeled_dir(files_to_upload)

if __name__ == "__main__":
    main()
