# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import sys
import os
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
    log_file_path = os.path.join(base_path, 'out', 'modeling_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")))

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)

    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'out'))])

def main(args=None):
    initialize()

    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    logging.info('Model generation starting at {}'.format(start_time))

    import sharedlib
    import config
    import modeler

    input_data_files = config.input_data_file_sets
    if len(args) > 0:
        logging.info('Generating model(s) for {}'.format(args[0]))
        input_data_files = [s for s in config.input_data_file_sets if args[0] in s['name']]
    modeler.generate_models_per_config(input_data_files)

    end_time = datetime.datetime.now()
    logging.info('Model generation completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading log file to Cloud...')
        sharedlib.upload_files_to_models_dir([log_file_path])

if __name__ == "__main__":
    main()
