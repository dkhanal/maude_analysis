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
    global models_dir
    global output_dir
    global target_file_max_num_records_to_classify
    global models
    global positive_probability_threshold
    global upload_output_to_cloud
    global upload_positive_files_only
    global cloud_blob_container_name
    global azure_account_name
    global azure_account_key
    global verbose

    input_data_files = config_data['input_data_files']
    output_dir = config_data['output_dir']
    models_dir = config_data['models_dir']
    models = config_data['models']
    target_file_max_num_records_to_classify = config_data['target_file_max_num_records_to_classify']
    positive_probability_threshold = config_data['positive_probability_threshold']
    verbose = config_data['verbose']

    upload_output_to_cloud = config_data['upload_output_to_cloud']
    upload_positive_files_only = config_data['upload_positive_files_only']
    cloud_blob_container_name = config_data['cloud_blob_container_name']

    if upload_output_to_cloud == True and ('azure_account_name' not in os.environ or 'azure_account_key' not in os.environ):
        logging.info('CONFIGURATION ERROR: Environment variable (azure_account_name) must be set to upload output files.')
    
    if upload_output_to_cloud == True:
        azure_account_name = os.environ['azure_account_name']    
        azure_account_key = os.environ['azure_account_key']

    logging.info('Configuration loaded.')

load_config()

