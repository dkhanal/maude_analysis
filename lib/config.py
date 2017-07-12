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
    global data_files_real_mode
    global data_files_sim_mode
    global data_file_record_limit
    global known_positive_records_limit
    global known_negative_records_limit
    global most_common_words_limit
    global verbose

    config_data_pos_section = config_data['known_positive_signals']
    known_positive_signals = [pre + ' ' + main for pre in config_data_pos_section['prefix_terms'] for main in config_data_pos_section['main_terms']]
    known_positive_signals += [main + ' ' + post for post in config_data_pos_section['postfix_terms'] for main in config_data_pos_section['main_terms']]

    potential_positive_signals = config_data['potential_positive_signals']['main_terms']

    output_files = config_data['output_files']
    data_files_real_mode = config_data['data_files_real_mode']
    data_files_sim_mode = config_data['data_files_sim_mode']
    data_file_record_limit = config_data['data_file_record_limit']
    known_positive_records_limit = config_data['known_positive_records_limit']
    known_negative_records_limit = config_data['known_negative_records_limit']
    most_common_words_limit = config_data['most_common_words_limit']
    verbose = config_data['verbose']

    print('Configuration loaded.')

load_config()

