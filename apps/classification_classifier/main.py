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

def upload_output_to_remote_server(pattern_to_match = None):
    import config
    import sharedlib

    if pattern_to_match is None:
        pattern_to_match = '.zip'

    logging.info('Uploading output of the previous run(s) to the remote server...')
    output_dir = sharedlib.abspath(config.output_dir)
    files_in_output_dir = os.listdir(output_dir)
    files_to_upload = [os.path.join(output_dir, f) for f in files_in_output_dir if f.lower().endswith(pattern_to_match)]
    sharedlib.upload_files_to_remote_server_with_prompt(files_to_upload, config.remote_server['classified_dir'])

def main(args=None):
    initialize()

    import config
    import classifier
    import sharedlib

    if args is None:
        args = sys.argv[1:]
    
    files_to_classify = config.files_to_classify
    if len(args) > 0:
        if 'upload' in args[0].lower():
            upload_output_to_remote_server(args[1] if len(args) > 1 else None)
            return

        logging.info('Argument: {}'.format(args[0]))
        files_to_classify = [s for s in config.files_to_classify if args[0] in s]
        logging.info(files_to_classify)

    start_time = datetime.datetime.now()
    logging.info('Classification of unknown records starting at {}'.format(start_time))

    classifier.classify_files(files_to_classify)

    end_time = datetime.datetime.now()
    logging.info('Classification completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading log file to Remote Server...')
        sharedlib.upload_files_to_classified_dir([log_file_path])

if __name__ == "__main__":
    main()

