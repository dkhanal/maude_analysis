# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import json
import logging

def get_config_file_path(hint_path):
    if hint_path is None:
        hint_path = '../config.json'

    if not os.path.isabs(hint_path):
        file = os.path.join(os.path.dirname(__file__), hint_path)
        logging.info('Config file is {}...'.format(file))
    else:
        file = hint_path
    return file

def load_config():
    logging.info('Loading configuration...')
    with open(get_config_file_path('../config.json')) as config_file:
        config_data = json.load(config_file)

    # Configuration items
    global files_to_classify
    global trained_trained_models_dir
    global output_dir
    global target_file_max_num_records_to_classify
    global models
    global positive_probability_threshold
    global upload_output_to_remote_server
    global upload_positive_files_only
    global remote_server
    global verbose

    files_to_classify = config_data['files_to_classify']
    output_dir = config_data['output_dir']
    trained_trained_models_dir = config_data['trained_trained_models_dir']
    models = config_data['models']
    target_file_max_num_records_to_classify = config_data['target_file_max_num_records_to_classify']
    positive_probability_threshold = config_data['positive_probability_threshold']

    upload_output_to_remote_server = config_data['upload_output_to_remote_server']
    upload_positive_files_only = config_data['upload_positive_files_only']

    remote_server = config_data['remote_server']
    verbose = config_data['verbose']

    logging.info('Configuration loaded.')

load_config()

