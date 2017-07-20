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
    global pickles_dir
    global output_dir
    global labeled_files_max_num_records_to_read
    global target_file_max_num_records_to_classify
    global classifiers
    global use_pickeled_models_if_present
    global positive_probability_threshold
    global verbose

    input_data_file_sets = config_data['input_data_file_sets']
    pickles_dir = config_data['pickles_dir']
    output_dir = config_data['output_dir']
    classifiers = config_data['classifiers']
    labeled_files_max_num_records_to_read = config_data['labeled_files_max_num_records_to_read']
    target_file_max_num_records_to_classify = config_data['target_file_max_num_records_to_classify']
    use_pickeled_models_if_present = config_data['use_pickeled_models_if_present']
    positive_probability_threshold = config_data['positive_probability_threshold']
    verbose = config_data['verbose']

    print('Configuration loaded.')

load_config()

