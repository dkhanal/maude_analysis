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
    log_file_path = os.path.join(base_path, 'out', 'pre_labeling_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")))

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)

    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'out')),
                           sharedlib.abspath(os.path.join(base_path, 'file_chunks'))])

def upload_output_to_remote_server(pattern_to_match = None):
    import config
    import sharedlib

    if pattern_to_match is None:
        pattern_to_match = '.zip'

    logging.info('Uploading output of the previous run(s) to the remote server...')
    output_dir = sharedlib.abspath(config.output_dir)
    files_in_output_dir = os.listdir(output_dir)
    files_to_upload = [os.path.join(output_dir, f) for f in files_in_output_dir if f.lower().endswith(pattern_to_match)]
    sharedlib.upload_files_to_remote_server_with_prompt(files_to_upload, config.remote_server['prelabeled_dir'])

def main(args=None):
    initialize()

    import config
    import extractor
    import sharedlib

    if args is None:
        args = sys.argv[1:]
    
    if len(args) > 0:
        if 'upload' in args[0].lower():
            upload_output_to_remote_server(args[1] if len(args) > 1 else None)
            return

        logging.info('Argument: {}'.format(args[0]))

    start_time = datetime.datetime.now()
    logging.info('Extracting potential positive and negative records starting at {}'.format(start_time))

    input_data_files = config.input_data_files
    if len(args) > 0:
        logging.info('Extracting for {}'.format(args[0]))
        input_data_files = [s for s in config.input_data_files if args[0] in s]
        logging.info(input_data_files)
    extractor.extract_records(input_data_files, config.output_dir, config.max_records_to_extract)

    end_time = datetime.datetime.now()
    logging.info('Extraction completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading log file to Remote Server...')
        sharedlib.upload_files_to_prelabeled_dir([log_file_path])


if __name__ == "__main__":
    main()
