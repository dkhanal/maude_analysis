import os
import sys
import datetime
import pickle
import codecs
import urllib
import platform
import random

import nltk
from nltk import word_tokenize

import config
import util
import uploader

def extract_features(list_of_words):
    features = {}
    for w in list_of_words:
        features[w] = True
    
    return features

def download_file(url, destination_path):
    file_path = os.path.abspath(destination_path)
    log('Downloading {} to {}. This may take a while...'.format(url, file_path))
    urllib.request.urlretrieve(url, file_path)

def create_models(input_data_files):
    output_dir = util.fix_path(config.output_dir)
    log_file_path = os.path.join(output_dir, 'process.log')

    global __log_file_handle
    __log_file_handle = open(log_file_path, 'w')

    start_time = datetime.datetime.now()
    process_log_first_line = 'MAUDE Modeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    log(process_log_first_line)
    log('modeler::create_models() starting at {}'.format(start_time))
    output_dir = util.fix_path(config.output_dir)
    input_dir = util.fix_path(config.input_dir)
    input_data_file_sets = config.input_data_file_sets
    models_config = config.models

    positive_file_features = []
    negative_file_features = []
    log('Checking if labeled archive(s) need to be downloaded...')
    for input_data_file_set in input_data_files:
        positive_records_file = os.path.join(input_dir, input_data_file_set['positive_records_file'])
        negative_records_file = os.path.join(input_dir, input_data_file_set['negative_records_file'])
        if input_data_file_set['always_download'] == True or os.path.exists(positive_records_file) == False or os.path.exists(negative_records_file) == False:
            log('Labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))
            download_zip_file_path = os.path.join(input_dir, input_data_file_set['name'] + '.zip')
            download_file(input_data_file_set['labeled_archive_url'], download_zip_file_path)
            log('Extracting labeled archive...')
            util.unzip(download_zip_file_path, input_dir)
            log('Labeled files extracted.')
        
        log('Positive records file: {}'.format(os.path.basename(positive_records_file)))
        log('Negative records file: {}'.format(os.path.basename(negative_records_file)))
        
        log('Building positive features...')
        positive_file_features += build_labeled_features(positive_records_file, 'pos', False, config.labeled_files_max_num_records_to_read)

        log('Building negative features...')
        negative_file_features += build_labeled_features(negative_records_file, 'neg', False, config.labeled_files_max_num_records_to_read)

    max_labeled_records_to_use = config.labeled_files_max_num_records_to_read
    if max_labeled_records_to_use is not None and len(positive_file_features) > max_labeled_records_to_use:
        log('Randomly taking {} records from {} positive features records...'.format(max_labeled_records_to_use, len(positive_file_features)))
        random.shuffle(positive_file_features)
        positive_file_features = positive_file_features[:max_labeled_records_to_use]

    if max_labeled_records_to_use is not None and len(negative_file_features) > max_labeled_records_to_use:
        log('Randomly taking {} records from {} negative features records...'.format(max_labeled_records_to_use, len(negative_file_features)))
        random.shuffle(negative_file_features)
        negative_file_features = negative_file_features[:max_labeled_records_to_use]

    training_set_cut_off_positive = int(len(positive_file_features) * .75)
    training_set_cut_off_negative = int(len(negative_file_features) * .75)

    training_featureset = positive_file_features[:training_set_cut_off_positive] + negative_file_features[:training_set_cut_off_negative]
    testing_featureset = positive_file_features[training_set_cut_off_positive:] + negative_file_features[training_set_cut_off_negative:]
    log('Model(s) will be trained on {} and tested on {} featureset instances. Training the model now (this may take a while)...'.format(len(training_featureset), len(testing_featureset)))

    for model_config in models_config:
        model_name = model_config['name'] 
        if model_name == 'naive_bayes_bow':
            log('Model in training:  nltk.classify.NaiveBayesClassifier')
            classifier = nltk.classify.NaiveBayesClassifier.train(training_featureset)

            log('Model trained. Assessing its accuracy now using the testing set... ')
            accuracy = nltk.classify.util.accuracy(classifier, testing_featureset)

            log('Model accuracy is: {}. '.format(accuracy))
            classifier.show_most_informative_features()

            pickle_file = util.fix_path(os.path.join(output_dir, model_name + '.pickle'))
            log('Pickling the model as: {}...'.format(os.path.basename(pickle_file)))
            util.pickle_object(classifier, pickle_file)
            log('Model pickled. '.format(accuracy))

            if config.upload_output_to_cloud == True:
                model_archive_name = model_name+'.zip'
                log('Uploading the pickled model ({}) to the Cloud...'.format(model_archive_name))
                uploader.upload_files([pickle_file], output_dir, os.path.join(output_dir, model_archive_name))

    end_time = datetime.datetime.now()
    log('modeler::create_models() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
    log('Uploading (best effort) logs now...')
    __log_file_handle.close()

    if config.upload_output_to_cloud == True:
        uploader.upload_files([log_file_path], output_dir, os.path.join(output_dir, 'log_{}.zip'.format(end_time.strftime("%Y%m%d-%H%M%S"))))

def build_labeled_features(file, label, skip_first_record=False, max_records = None):
    log('Building ({}) features for file {}...'.format(label, file))
    file_features = []
    file_base_name = os.path.basename(file)
    total_records = 0
    total_data_records = 0
    fin = codecs.open(file, encoding='utf-8', errors='ignore')
    for record in fin:
        total_records += 1
        sys.stdout.write('{} => Now processing record: {}...\r'.format(file_base_name, total_records))
        sys.stdout.flush()

        if total_records == 1 and skip_first_record == True:
            continue
            
        total_data_records += 1

        if max_records is not None and total_data_records > max_records:
            break

        record_lower_case = record.lower()
        record_words = word_tokenize(record_lower_case)
        record_features = extract_features(record_words)

        if label == None:
            file_features.append(record_features)
        else:
            file_features.append((record_features, label))
    
    fin.close()
    log('{} => Total {} record(s) processed.'.format(file_base_name, total_data_records))
    return file_features

def log(line):
    __log_file_handle.write(line + '\n')
    print(line)
