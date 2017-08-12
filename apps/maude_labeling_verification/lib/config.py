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
    global cloud_files
    global output_files
    global input_dir
    global upload_output_to_cloud
    global azure_account_name
    global azure_account_key
    global verbose

    input_data_file_sets = config_data['input_data_file_sets']
    cloud_files = config_data['cloud_files']
    output_files = config_data['output_files']
    input_dir = config_data['input_dir']
    upload_output_to_cloud = config_data['upload_output_to_cloud']
    verbose = config_data['verbose']
        
    if upload_output_to_cloud == True:
        azure_account_name = os.environ['azure_account_name']    
        azure_account_key = os.environ['azure_account_key']


    print('Configuration loaded.')

load_config()

