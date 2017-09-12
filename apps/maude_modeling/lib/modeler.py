# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import datetime
import pickle
import codecs
import urllib
import platform
import random
import hashlib
import re
import string
import logging

import nltk

import sharedlib
import config
import nltk_naive_bayes

def log(line):
    logging.info(line)


def generate_models(positive_records_files, negative_records_files, models_config, output_dir, upload_generated_models_to_remote_server):
    output_dir = sharedlib.abspath(output_dir)
    start_time = datetime.datetime.now()
    log('modeler::generate_models() starting at {}'.format(start_time))
    process_log_first_line = 'MAUDE Modeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)

    log(process_log_first_line)

    generated_models = []

    for model_config in models_config:
        model_start_time = datetime.datetime.now()
        model_name = model_config['name']
        log('Starting model generation for: {} at {}...'.format(model_name, model_start_time))

        classifier, all_pos_records_file_path, all_neg_records_file_path  = nltk_naive_bayes.generate_model(positive_records_files, negative_records_files, model_config, output_dir)

        pickle_file = sharedlib.abspath(os.path.join(output_dir, model_name + '.pickle'))
        logging.info('Pickling the model as: {}...'.format(os.path.basename(pickle_file)))
        sharedlib.pickle_object(classifier, pickle_file)
        logging.info('Model pickled.')

        generated_models.append((model_name, pickle_file))

        if upload_generated_models_to_remote_server == True:
            model_archive_name = model_name+'.zip'
            zipped_file = sharedlib.zip_files([pickle_file, all_pos_records_file_path, all_neg_records_file_path], sharedlib.abspath(os.path.join(output_dir, model_archive_name)))
            log('Uploading the pickled model ({}) to the Remote Server...'.format(model_archive_name))
            sharedlib.upload_files_to_models_dir([zipped_file])

        model_end_time = datetime.datetime.now()
        log('Completed creating model for: {} at {}. Duration: {}...'.format(model_name, model_end_time, model_end_time - model_start_time))

    end_time = datetime.datetime.now()
    return generated_models

def generate_models_per_config(input_data_files):
    input_dir = sharedlib.abspath(config.input_dir)
    output_dir = sharedlib.abspath(config.output_dir)
    start_time = datetime.datetime.now()
    log('modeler::create_models() starting at {}'.format(start_time))

    positive_records_files = []
    negative_records_files = []
    log('Checking if labeled archive(s) need to be downloaded...')
    for input_data_file_set in input_data_files:
        positive_records_file = os.path.join(input_dir, input_data_file_set['positive_records_file'])
        negative_records_file = os.path.join(input_dir, input_data_file_set['negative_records_file'])
        if input_data_file_set['always_download'] == True or os.path.exists(positive_records_file) == False or os.path.exists(negative_records_file) == False:
            log('Labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))
            sharedlib.download_file(input_data_file_set['base_url'] +  input_data_file_set['positive_records_file'], positive_records_file)
            sharedlib.download_file(input_data_file_set['base_url'] +  input_data_file_set['negative_records_file'], negative_records_file)

        log('Positive records file: {}'.format(os.path.basename(positive_records_file)))
        log('Negative records file: {}'.format(os.path.basename(negative_records_file)))

        positive_records_files.append(positive_records_file)
        negative_records_files.append(negative_records_file)

        generate_models(positive_records_files, negative_records_files, config.models, output_dir, config.upload_output_to_remote_server)