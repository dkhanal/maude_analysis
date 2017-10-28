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
    global input_data_files
    global remote_server_files
    global output_files
    global regen_models
    global auto_regen_models
    global models_auto_regen_records_threshold
    global models
    global models_output_dir
    global upload_regenerated_models_to_remote_server
    global input_dir
    global output_dir
    global upload_output_to_remote_server
    global remote_server
    global min_probability_for_auto_labeling
    global min_model_score_for_auto_labeling
    global percent_of_new_records_to_qc
    global duplicate_record_check_ignore_pattern
    global verbose

    input_data_files = config_data['input_data_files']
    remote_server_files = config_data['remote_server_files']
    output_files = config_data['output_files']
    input_dir = config_data['input_dir']
    output_dir = config_data['output_dir']
    upload_output_to_remote_server = config_data['upload_output_to_remote_server']

    regen_models = config_data['regen_models']
    auto_regen_models = config_data['auto_regen_models']
    models_auto_regen_records_threshold = config_data['models_auto_regen_records_threshold']
    models = config_data['models']
    models_output_dir = config_data['models_output_dir']
    upload_regenerated_models_to_remote_server = config_data['upload_regenerated_models_to_remote_server']
    remote_server = config_data['remote_server']

    min_probability_for_auto_labeling = config_data['min_probability_for_auto_labeling']
    min_model_score_for_auto_labeling = config_data['min_model_score_for_auto_labeling']
    percent_of_new_records_to_qc = config_data['percent_of_new_records_to_qc']
    duplicate_record_check_ignore_pattern = config_data['duplicate_record_check_ignore_pattern']

    verbose = config_data['verbose']

    logging.info('Configuration loaded.')

load_config()

