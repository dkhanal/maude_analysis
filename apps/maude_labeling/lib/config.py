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
    global known_positive_records_qualifying_terms
    global potential_positive_records_qualifying_terms
    global known_positive_records_disqualifying_terms
    global input_data_files
    global output_dir
    global max_records_to_extract
    global verbose

    config_data_pos_section = config_data['known_positive_records_selection_terms']
    known_positive_records_qualifying_terms = [pre + ' ' + main for pre in config_data_pos_section['qualifying_prefix_terms'] for main in config_data_pos_section['qualifying_main_terms']]
    known_positive_records_qualifying_terms += [' ' +main + ' ' + post for post in config_data_pos_section['qualifying_postfix_terms'] for main in config_data_pos_section['qualifying_main_terms']]
    known_positive_records_qualifying_terms += config_data_pos_section['standalone_patterns'] 
 
    known_positive_records_disqualifying_terms = [pre + term for pre in config_data_pos_section['disqualifying_negative_prefix_patterns'] for term in  known_positive_records_qualifying_terms]
    known_positive_records_disqualifying_terms += [term + post for post in config_data_pos_section['disqualifying_negative_postfix_patterns'] for term in  known_positive_records_qualifying_terms]

    potential_positive_records_qualifying_terms = config_data['known_positive_records_selection_terms']['qualifying_main_terms']  + config_data['potential_positive_records_selection_terms']['qualifying_main_terms']

    input_data_files = config_data['input_data_files']
    output_dir = config_data['output_dir']
    max_records_to_extract = config_data['max_records_to_extract']
    verbose = config_data['verbose']

    print('Configuration loaded.')

load_config()

