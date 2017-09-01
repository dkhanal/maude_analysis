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
    global known_positive_records_qualifying_terms
    global potential_positive_records_qualifying_terms
    global known_positive_records_disqualifying_terms
    global input_data_files
    global output_dir
    global file_split_dir
    global file_split_lines_per_file
    global max_records_to_extract
    global match_extracted_positive_negative_records_count
    global upload_output_to_remote_server
    global remote_server

    global verbose

    config_data_pos_section = config_data['known_positive_records_selection_terms']
    known_positive_records_qualifying_terms = [pre + ' ' + main for pre in config_data_pos_section['qualifying_prefix_terms'] for main in config_data_pos_section['qualifying_main_terms']]
    known_positive_records_qualifying_terms += [' ' +main + ' ' + post for post in config_data_pos_section['qualifying_postfix_terms'] for main in config_data_pos_section['qualifying_main_terms']]
    known_positive_records_qualifying_terms += config_data_pos_section['standalone_patterns'] 
 
    known_positive_records_disqualifying_terms = [pre + term for pre in config_data_pos_section['disqualifying_prefix_patterns'] for term in  known_positive_records_qualifying_terms]
    known_positive_records_disqualifying_terms += [term + post for post in config_data_pos_section['disqualifying_postfix_patterns'] for term in  known_positive_records_qualifying_terms]
    known_positive_records_disqualifying_terms += [term for term in config_data_pos_section['disqualifying_standalone_patterns']]

    potential_positive_records_qualifying_terms = config_data['known_positive_records_selection_terms']['qualifying_main_terms']  + config_data['potential_positive_records_selection_terms']['qualifying_main_terms']

    input_data_files = config_data['input_data_files']
    output_dir = config_data['output_dir']
    file_split_dir = config_data['file_split_dir']
    file_split_lines_per_file = config_data['file_split_lines_per_file']

    max_records_to_extract = config_data['max_records_to_extract']
    match_extracted_positive_negative_records_count = config_data['match_extracted_positive_negative_records_count']

    upload_output_to_remote_server = config_data['upload_output_to_remote_server']
    remote_server = config_data['remote_server']

    verbose = config_data['verbose']

    logging.info('Configuration loaded.')

load_config()