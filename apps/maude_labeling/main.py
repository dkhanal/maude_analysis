# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import sys
import os
import re

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

    global log_file_path
    log_file_path = os.path.join(base_path, 'out', 'labeling_{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")))

    import config
    import sharedlib
    sharedlib.initialize(base_path, log_file_path, config.remote_server)
    
    sharedlib.create_dirs([sharedlib.abspath(os.path.join(base_path, 'in')),
                           sharedlib.abspath(os.path.join(base_path, 'out')),
                           sharedlib.abspath(os.path.join(base_path, '..', 'maude_modeling', 'out'))
                           ])

def upload_output_to_remote_server(also_uplaod_merged_input_files):
    import config
    import sharedlib

    logging.info('Uploading output of the previous run(s) to the remote server...')

    output_files = config.output_files

    files_to_upload = [
        sharedlib.abspath(output_files['verified_positive_records_file']),
        sharedlib.abspath(output_files['verified_negative_records_file']),
        sharedlib.abspath(output_files['already_processed_record_numbers_file'])
        ]

    output_dir = sharedlib.abspath(config.output_dir)

    accuracy_file_pattern = re.compile('.*_accuracy.json')
    accuarcy_files = [sharedlib.abspath(os.path.join(output_dir, file_name)) for file_name in os.listdir(output_dir) if re.search(accuracy_file_pattern, file_name) is not None]
    
    files_to_upload += accuarcy_files

    if also_uplaod_merged_input_files == True:
        files_to_upload += [
        sharedlib.abspath(output_files['potential_positive_records_file']),
        sharedlib.abspath(output_files['potential_negative_records_file']),
        sharedlib.abspath(output_files['questionable_positive_records_file']),
        sharedlib.abspath(output_files['questionable_negative_records_file'])
        ]

    files_to_upload = [f for f in files_to_upload if os.path.exists(f) == True]
    sharedlib.upload_files_to_remote_server_with_prompt(files_to_upload, config.remote_server['labeled_dir'])

def main(args=None):
    initialize()

    import config
    import labeler
    import sharedlib

    if args is None:
        args = sys.argv[1:]
    
    if len(args) > 0:    
        if 'upload' in args[0].lower():
            upload_output_to_remote_server(len(args) > 1 and args[1].lower() in 'all')
            return

        logging.info('Argument: {}'.format(args[0]))


    os.system('mode con: cols=200')
    start_time = datetime.datetime.now()
    logging.info('Manually verifying pre-labeled records starting at {}'.format(start_time))
    
    mode = None

    if len(args) > 0 and (args[0] == 'pos' or args[0] == 'pos?' or args[0] == 'neg' or args[0] == 'neg?'):
        mode = args[0]

    logging.info('Labeling records. Mode: {}'.format(mode))

    labeler.label_records(mode)

    end_time = datetime.datetime.now()
    logging.info('Manual verification session completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading log file to Remote Server...')
        sharedlib.upload_files_to_labeled_dir([log_file_path])

if __name__ == "__main__":
    main()
