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
import _nltk_naive_bayes
import _sklearn

def log(line):
    logging.info(line)


def generate_models(positive_records_files, negative_records_files, models_config, duplicate_record_check_ignore_pattern,  output_dir, upload_generated_models_to_remote_server):
    output_dir = sharedlib.abspath(output_dir)
    start_time = datetime.datetime.now()
    log('modeler::generate_models() starting at {}'.format(start_time))
    process_log_first_line = 'MAUDE Modeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)

    log(process_log_first_line)

    log('Merging all positive/negative labeled files. Two sets (all and one without duplicate records) will be produced...')

    all_pos_records_file_path = os.path.join(output_dir, 'positive_records_all.txt')
    all_neg_records_file_path = os.path.join(output_dir,'negative_records_all.txt')

    nodups_pos_records_file_path = os.path.join(output_dir, 'positive_records_nodups.txt')
    nodups_neg_records_file_path = os.path.join(output_dir,'negative_records_nodups.txt')

    sharedlib.merge_files([sharedlib.abspath(p) for p in positive_records_files], all_pos_records_file_path, False, None)
    sharedlib.merge_files([sharedlib.abspath(p) for p in negative_records_files], all_neg_records_file_path, False, None)

    sharedlib.merge_files([sharedlib.abspath(p) for p in positive_records_files], nodups_pos_records_file_path, True, duplicate_record_check_ignore_pattern)
    sharedlib.merge_files([sharedlib.abspath(p) for p in negative_records_files], nodups_neg_records_file_path, True, duplicate_record_check_ignore_pattern)

    sharedlib.randomize_records(all_pos_records_file_path)
    sharedlib.randomize_records(nodups_pos_records_file_path)
    sharedlib.randomize_records(all_neg_records_file_path)
    sharedlib.randomize_records(nodups_neg_records_file_path)

    log('Combined (merged and randomized) positive labeled (all) file: {}'.format(all_pos_records_file_path))
    log('Combined (merged and randomized) positive labeled (no-duplicates) file: {}'.format(nodups_pos_records_file_path))
    log('Combined (merged and randomized) negative labeled (all) file: {}'.format(all_neg_records_file_path))
    log('Combined (merged and randomized) negative labeled (no-duplicates) file: {}'.format(nodups_neg_records_file_path))

    generated_models = []

    for model_config in models_config:
        model_start_time = datetime.datetime.now()
        model_name = model_config['name']
        log('Starting model generation for: {} at {}...'.format(model_name, model_start_time))

        pos_labeled_file_path = None
        neg_labeled_file_path = None

        if 'nltk.naive_bayes' in model_name or 'sklearn' in model_name:
            if model_config['ignore_duplicate_training_records'] == True:
                pos_labeled_file_path = nodups_pos_records_file_path
                neg_labeled_file_path = nodups_neg_records_file_path
            else:
                pos_labeled_file_path = all_pos_records_file_path
                neg_labeled_file_path = all_neg_records_file_path
        else:
            raise ValueError('Unsupported model: {}'.format(model_name))

        classifier = None
        vectorizer = None
        score = None

        if 'nltk.naive_bayes' in model_name:
            classifier, score = _nltk_naive_bayes.generate_model(pos_labeled_file_path, neg_labeled_file_path, model_config, output_dir)
        else:
            classifier, vectorizer, score = _sklearn.generate_model(pos_labeled_file_path, neg_labeled_file_path, model_config, output_dir)

        classifier_pickle_file = sharedlib.abspath(os.path.join(output_dir, model_name + '.pickle'))
        logging.info('Pickling the model as: {}...'.format(os.path.basename(classifier_pickle_file)))
        sharedlib.pickle_object(classifier, classifier_pickle_file)

        vectorizer_pickle_file = None
        if vectorizer is not None:
            vectorizer_pickle_file = sharedlib.abspath(os.path.join(output_dir, model_name + '.vectorizer.pickle'))
            logging.info('Pickling the Vectorizer as: {}...'.format(os.path.basename(vectorizer_pickle_file)))
            sharedlib.pickle_object(vectorizer, vectorizer_pickle_file)

        logging.info('Model pickled.')

        generated_models.append((model_name, classifier_pickle_file, vectorizer_pickle_file, score))

        if upload_generated_models_to_remote_server == True:
            model_archive_name = model_config['archive_name']

            files_to_zip = [pos_labeled_file_path, neg_labeled_file_path, classifier_pickle_file]
            if vectorizer is not None:
                files_to_zip.append(vectorizer_pickle_file)

            zipped_file = sharedlib.zip_files(files_to_zip, sharedlib.abspath(os.path.join(output_dir, model_archive_name)))
            log('Uploading the pickled model ({}) to the Remote Server...'.format(model_archive_name))
            sharedlib.upload_files_to_trained_models_dir([zipped_file])

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
            log('Labeled archive for input data needs to be downloaded.')
            positive_records_file_uri = sharedlib.join_remote_server_paths(config.remote_server['base_uri'], input_data_file_set['remote_blob_dir'], input_data_file_set['positive_records_file'])
            negative_records_file_uri = sharedlib.join_remote_server_paths(config.remote_server['base_uri'], input_data_file_set['remote_blob_dir'], input_data_file_set['negative_records_file'])
            sharedlib.download_file(positive_records_file_uri, positive_records_file, True)
            sharedlib.download_file(negative_records_file_uri, negative_records_file, True)

        log('Positive records file: {}'.format(os.path.basename(positive_records_file)))
        log('Negative records file: {}'.format(os.path.basename(negative_records_file)))

        positive_records_files.append(positive_records_file)
        negative_records_files.append(negative_records_file)

        generate_models(positive_records_files, negative_records_files, config.models, config.duplicate_record_check_ignore_pattern, output_dir, config.upload_output_to_remote_server)