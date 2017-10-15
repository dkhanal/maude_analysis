# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import urllib
import logging
import re

import sharedlib

def download_remote_server_files(remote_server_config, remote_server_files, output_files):
    labeled_base_uri = sharedlib.join_remote_server_paths(remote_server_config['base_uri'], remote_server_config['labeled_dir'])
    logging.info('Downloading cloud files from {}'.format(labeled_base_uri))

    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['potential_positive_records_blob']),
                  sharedlib.abspath(output_files['potential_positive_records_file']),
                  not remote_server_files['skip_download_if_already_present'])
    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['potential_negative_records_blob']),
                            sharedlib.abspath(output_files['potential_negative_records_file']),
                  not remote_server_files['skip_download_if_already_present'])
    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['questionable_positive_records_blob']),
                            sharedlib.abspath(output_files['questionable_positive_records_file']),
                  not remote_server_files['skip_download_if_already_present'])
    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['questionable_negative_records_blob']),
                            sharedlib.abspath(output_files['questionable_negative_records_file']),
                  not remote_server_files['skip_download_if_already_present'])

    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['verified_positive_records_blob']),
                            sharedlib.abspath(output_files['verified_positive_records_file']), True)
    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['verified_negative_records_blob']),
                            sharedlib.abspath(output_files['verified_negative_records_file']), True)
    sharedlib.download_file(sharedlib.join_remote_server_paths(labeled_base_uri, remote_server_files['already_processed_record_numbers_blob']),
                            sharedlib.abspath(output_files['already_processed_record_numbers_file']), True)

    logging.info('Downloading model labeling accuracy files...')
    accuracy_file_pattern = re.compile('.*_accuracy.json')
    remote_files = sharedlib.get_list_of_files_from_remote_server(remote_server_config['labeled_dir'])
    accuarcy_files = [file_name for file_name in remote_files if re.search(accuracy_file_pattern, file_name) is not None]

    for accuracy_file in accuarcy_files:
        file_uri = sharedlib.join_remote_server_paths(labeled_base_uri, accuracy_file)
        file_local_path = sharedlib.abspath(os.path.join(os.path.dirname(output_files['already_processed_record_numbers_file']), accuracy_file)) 
        sharedlib.download_file(file_uri, file_local_path, True)

def download_models_from_remote_server(remote_server_config, models_config, output_dir):
    logging.info('Downloading models...')
    output_dir = sharedlib.abspath(output_dir)
    remote_files = sharedlib.get_list_of_files_from_remote_server(remote_server_config['models_dir'])
    
    models_base_uri = sharedlib.join_remote_server_paths(remote_server_config['base_uri'], remote_server_config['models_dir'])

    models = []
    for model_config in models_config:
        name_zip_tuple = (model_config['name'], model_config['archive_name'], os.path.join(output_dir, model_config['archive_name']))
        classifier = None
        vectorizer = None
        if name_zip_tuple[1] in remote_files:
            sharedlib.download_file(sharedlib.join_remote_server_paths(models_base_uri,  model_config['archive_name']), name_zip_tuple[2], True)
            sharedlib.unzip(name_zip_tuple[2], output_dir)
            pickle_file = os.path.join(output_dir, name_zip_tuple[0] + '.pickle')
            if os.path.exists(pickle_file):
                classifier = sharedlib.load_pickle(pickle_file)

        vectorizer_pickle_file = os.path.join(output_dir, name_zip_tuple[0] + '.vectorizer.pickle')
        if os.path.exists(vectorizer_pickle_file):
            logging.info('Vectorizer pickle file: {}'.format(os.path.basename(vectorizer_pickle_file)))
            logging.info('Loading the pickled vectorizer...')
            vectorizer = sharedlib.load_pickle(vectorizer_pickle_file)
        else:
            logging.info('No vectorizer (expected: {}) found for this model.'.format(vectorizer_pickle_file))

        if classifier is not None:
            models.append((name_zip_tuple[0], classifier, vectorizer))
        else:
            logging.info('Could not find pickled classifier in the package {} on the Remote Server'.format( name_zip_tuple[1]))

    logging.info('{} MODELS LOADED'.format(len(models)))
    return models

def all_work_in_progress_files_present_on_remote_server(remote_server_config, remote_server_files):
    logging.info('Checking for the presence of cloud files...')
    remote_files = sharedlib.get_list_of_files_from_remote_server(remote_server_config['labeled_dir'])
    if not remote_server_files['potential_positive_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['potential_positive_records_blob']))
        return False

    if not remote_server_files['potential_negative_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['potential_negative_records_blob']))
        return False

    if not remote_server_files['questionable_positive_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['questionable_positive_records_blob']))
        return False

    if not remote_server_files['questionable_negative_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['questionable_negative_records_blob']))
        return False

    if not remote_server_files['verified_positive_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['verified_positive_records_blob']))
        return False

    if not remote_server_files['verified_negative_records_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['verified_negative_records_blob']))
        return False

    if not remote_server_files['already_processed_record_numbers_blob'] in remote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['already_processed_record_numbers_blob']))
        return False

    return True
