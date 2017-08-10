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
    global input_data_files
    global positive_records_output_file
    global negative_records_output_file
    global last_processed_record_number_file
    global verbose

    input_data_files = config_data['input_data_files']
    positive_records_output_file = config_data['positive_records_output_file']
    negative_records_output_file = config_data['negative_records_output_file']
    last_processed_record_number_file = config_data['last_processed_record_number_file']
    verbose = config_data['verbose']

    print('Configuration loaded.')

load_config()

