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
    global known_positive_signals
    global potential_positive_signals
    global output_files
    global data_files_for_featureset
    global data_files_for_classification
    global data_file_max_num_rows_for_featureset
    global data_file_max_num_rows_to_classify
    global tag_positive
    global tag_negative
    global known_positive_records_limit
    global known_negative_records_limit
    global positive_probability_threshold
    global most_common_words_limit
    global output_positive_record_id_only
    global verbose

    config_data_pos_section = config_data['known_positive_signals']
    known_positive_signals = [pre + ' ' + main for pre in config_data_pos_section['prefix_terms'] for main in config_data_pos_section['main_terms']]
    known_positive_signals += [main + ' ' + post for post in config_data_pos_section['postfix_terms'] for main in config_data_pos_section['main_terms']]

    potential_positive_signals = config_data['known_positive_signals']['main_terms'] + config_data['potential_positive_signals']['main_terms']

    output_files = config_data['output_files']
    data_files_for_featureset = config_data['data_files_for_featureset']
    data_files_for_classification = config_data['data_files_for_classification']
    tag_positive = config_data['tag_positive']
    tag_negative = config_data['tag_negative']
    data_file_max_num_rows_for_featureset = config_data['data_file_max_num_rows_for_featureset']
    data_file_max_num_rows_to_classify = config_data['data_file_max_num_rows_to_classify']
    known_positive_records_limit = config_data['known_positive_records_limit']
    known_negative_records_limit = config_data['known_negative_records_limit']
    positive_probability_threshold = config_data['positive_probability_threshold']
    most_common_words_limit = config_data['most_common_words_limit']
    output_positive_record_id_only = config_data['output_positive_record_id_only']
    verbose = config_data['verbose']

    print('Configuration loaded.')

load_config()

