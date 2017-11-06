# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os

import modeler
import logging
import config
import sharedlib

def rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file):
    logging.info('Rebuilding models...')
    if config.regen_models is None or config.regen_models == False:
        logging.info('Configuration does NOT allow regeneration of the models.')
        return None

    models_config = config.models
    upload_regenerated_models_to_remote_server = config.upload_regenerated_models_to_remote_server    

    if config.upload_output_to_remote_server == True:
        logging.info('Uploading labeled records so far to Cloud...')
        files_to_upload = [verified_positive_records_file_path, verified_negative_records_file_path,
                           already_processed_record_numbers_file]
        sharedlib.upload_files_to_labeling_verified_samples_dir(files_to_upload)

    logging.info('Generating models...')
    model_pickles = modeler.generate_models([verified_positive_records_file_path],
                                            [verified_negative_records_file_path],
                                            models_config,
                                            config.duplicate_record_check_ignore_pattern,
                                            config.models_output_dir,
                                            upload_regenerated_models_to_remote_server
                                            )
    models = []

    for model_name_pickle_tuple in model_pickles:
        if os.path.exists(model_name_pickle_tuple[1]):
            classifier = sharedlib.load_pickle(model_name_pickle_tuple[1])
            vectorizer = None
            if model_name_pickle_tuple[2] is not None:
                vectorizer = sharedlib.load_pickle(model_name_pickle_tuple[2])

            models.append((model_name_pickle_tuple[0], classifier, vectorizer))

    logging.info('*** {} MODELS REBUILT ***'.format(len(models)))
    return models