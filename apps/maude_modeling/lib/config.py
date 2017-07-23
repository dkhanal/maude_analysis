# By Deepak Khanal
# dkhanal@gmail.com

import os
import json

def get_config_file_path(hint_path):
    if hint_path is None:
        hint_path = '../config.json'

    if not os.path.isabs(hint_path):
        file = os.path.join(os.path.dirname(__file__), hint_path)
        print('Config file is {}...'.format(file))
    else:
        file = hint_path
    return file

def load_config():
    print('Loading configuration...')
    with open(get_config_file_path('../config.json')) as config_file:
        config_data = json.load(config_file)

    # Configuration items
    global input_data_file_sets
    global input_dir
    global output_dir
    global labeled_files_max_num_records_to_read
    global models
    global upload_output_to_cloud
    global cloud_blob_container_name
    global azure_account_name
    global azure_account_key
    global verbose

    input_data_file_sets = config_data['input_data_file_sets']
    input_dir = config_data['input_dir']
    output_dir = config_data['output_dir']
    models = config_data['models']
    upload_output_to_cloud = config_data['upload_output_to_cloud']
    cloud_blob_container_name = config_data['cloud_blob_container_name']
    labeled_files_max_num_records_to_read = config_data['labeled_files_max_num_records_to_read']
    verbose = config_data['verbose']

    if upload_output_to_cloud == True and ('azure_account_name' not in os.environ or 'azure_account_key' not in os.environ):
        print('CONFIGURATION ERROR: Environment variable (azure_account_name) must be set to upload output files.')
    
    if upload_output_to_cloud == True:
        azure_account_name = os.environ['azure_account_name']    
        azure_account_key = os.environ['azure_account_key']

    print('Configuration loaded.')

load_config()

