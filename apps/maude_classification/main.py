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

    import sharedlib
    sharedlib.set_current_app_path(__file__)

    global log_file_path
    log_file_path = sharedlib.abspath(os.path.join(base_path, 'out', 'classification_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))))

    sharedlib.initialize_logger(sharedlib.abspath(log_file_path))
    sharedlib.load_environment_vars(sharedlib.abspath(os.path.join(base_path, '.setenv.py')))
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
    
    input_data_files = config.input_data_files
    if len(args) > 0:
        logging.info('Classifying {}'.format(args[0]))
        input_data_files = [s for s in config.input_data_files if args[0] in s]
        logging.info(input_data_files)


    classifier.classify(input_data_files)

    end_time = datetime.datetime.now()
    logging.info('Classification completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_cloud == True:
        sharedlib.upload_files_to_cloud_container([log_file_path], config.cloud_blob_container_name)

if __name__ == "__main__":
    main()

