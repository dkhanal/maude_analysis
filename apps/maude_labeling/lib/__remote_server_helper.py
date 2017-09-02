# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import urllib
import logging

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

def download_models_from_remote_server(remote_server_config, models_config, output_dir):
    logging.info('Downloading models...')
    output_dir = sharedlib.abspath(output_dir)
    remote_files = sharedlib.get_list_of_files_from_remote_server(remote_server_config['models_dir'])
    
    models_base_uri = sharedlib.join_remote_server_paths(remote_server_config['base_uri'], remote_server_config['models_dir'])

    models = []
    for model_config in models_config:

        name_zip_tuple = (model_config['name'], model_config['archive_name'], os.path.join(output_dir, model_config['archive_name']))
        if name_zip_tuple[1] in remote_files:

            sharedlib.download_file(sharedlib.join_remote_server_paths(models_base_uri,  model_config['archive_name']), name_zip_tuple[2])
            sharedlib.unzip(name_zip_tuple[2], output_dir)
            pickle_file = os.path.join(output_dir, name_zip_tuple[0] + '.pickle')
            if os.path.exists(pickle_file):
                model = sharedlib.load_pickle(pickle_file)
                models.append((name_zip_tuple[0], model))
        else:
            logging.info('Could not find model file {} on the Remote Server'.format( name_zip_tuple[1]))

    logging.info('{} MODELS LOADED'.format(len(models)))
    return models

def all_work_in_progress_files_present_on_remote_server(remote_server_config, remote_server_files):
    logging.info('Checking for the presence of cloud files...')
    remote_files = sharedlib.get_list_of_files_from_remote_server(remote_server_config['models_dir'])
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

    if not remote_server_files['already_processed_record_numbers_blob'] in blobsremote_files:
        logging.info('Could not find file {} on the Remote Server'.format(remote_server_files['already_processed_record_numbers_blob']))
        return False

    return True