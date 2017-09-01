# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import sys
import os

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
    add_to_path(os.path.abspath(os.path.join(base_path, '..', 'maude_modeling', 'lib')))
    add_to_path(os.path.abspath(os.path.join(base_path, '..', 'maude_classification', 'lib')))

    import sharedlib
    sharedlib.set_current_app_path(__file__)

    global log_file_path
    log_file_path = sharedlib.abspath(os.path.join(base_path, 'out', 'labeling_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))))
    sharedlib.initialize_logger(sharedlib.abspath(os.path.join(base_path, 'out', log_file_path)))

    sharedlib.load_environment_vars(sharedlib.abspath(os.path.join(base_path, '.setenv.py')))
    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'in')),
                           sharedlib.abspath(os.path.join(base_path, 'out')),
                           sharedlib.abspath(os.path.join(base_path, '..', 'maude_modeling', 'out'))
                           ])
def main(args=None):
    initialize()

    os.system('mode con: cols=200 lines=50')

    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    logging.info('Manually verifying pre-labeled records starting at {}'.format(start_time))
    
    mode = None

    if len(args) > 0 and (args[0] == 'pos' or args[0] == 'pos?' or args[0] == 'neg' or args[0] == 'neg?'):
        mode = args[0]
        return

    logging.info('Labeling records. Mode: {}'.format(mode))

    import config
    import labeler
    import sharedlib

    labeler.label_records(mode)


    end_time = datetime.datetime.now()
    logging.info('Manual verification session completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_cloud == True:
        logging.info('Uploading log file to Cloud...')
        sharedlib.upload_files_to_cloud_container([log_file_path], config.cloud_files['container'])

if __name__ == "__main__":
    main()
