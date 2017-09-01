# Copyright (c) 2017 Deepak Khanal.
# All Rights Reserved.
# Email: dkhanal@gmail.com

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
    log_file_path = os.path.join(base_path, 'out', 'classification_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")))

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)

    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'in')), sharedlib.abspath(os.path.join(base_path, 'models')), sharedlib.abspath(os.path.join(base_path, 'out'))])

def main(args=None):
    initialize()

    import config
    import classifier
    import sharedlib

    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    logging.info('Classification of unknown records starting at {}'.format(start_time))
    
    files_to_classify = config.files_to_classify
    if len(args) > 0:
        logging.info('Classifying {}'.format(args[0]))
        files_to_classify = [s for s in config.files_to_classify if args[0] in s]
        logging.info(files_to_classify)


    classifier.classify(files_to_classify)

    end_time = datetime.datetime.now()
    logging.info('Classification completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading log file to Cloud...')
        sharedlib.upload_files_to_classification_dir([log_file_path])

if __name__ == "__main__":
    main()

