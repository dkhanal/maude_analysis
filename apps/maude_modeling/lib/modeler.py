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
    log('modeler::create_models() starting at {}'.format(start_time))
    process_log_first_line = 'MAUDE Modeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    log(process_log_first_line)

    for model_config in config.models:
        model_start_time = datetime.datetime.now()
        model_name = model_config['name'] 
        log('Starting model generation for: {} at {}...'.format(model_name, start_time))

        labeled_files_max_num_records_to_read = model_config['labeled_files_max_num_records_to_read']
        max_num_labeled_records_to_use = model_config['max_num_labeled_records_to_use']
        ignore_duplicate_training_records = model_config['ignore_duplicate_training_records']

        duplicate_check_ignore_pattern = None

        if  ignore_duplicate_training_records == True:
            duplicate_check_ignore_pattern = model_config['duplicate_check_ignore_pattern']

        if duplicate_check_ignore_pattern is not None:
            duplicate_check_ignore_pattern = re.compile(duplicate_check_ignore_pattern, re.IGNORECASE)

        record_hash_dict = {}

        all_pos_records_file_path = os.path.join(output_dir, model_name+'_positive_featureset_records.txt')
        all_neg_records_file_path = os.path.join(output_dir, model_name+'_negative_featureset_records.txt')

        all_pos_records_file = codecs.open(all_pos_records_file_path, 'w', encoding='utf-8', errors='ignore')
        all_neg_records_file = codecs.open(all_neg_records_file_path, 'w', encoding='utf-8', errors='ignore')

        output_dir = util.fix_path(config.output_dir)
        input_dir = util.fix_path(config.input_dir)
        models_config = config.models

        positive_file_features = []
        negative_file_features = []
        log('Checking if labeled archive(s) need to be downloaded...')
        for input_data_file_set in input_data_files:
            positive_records_file = os.path.join(input_dir, input_data_file_set['positive_records_file'])
            negative_records_file = os.path.join(input_dir, input_data_file_set['negative_records_file'])
            if input_data_file_set['always_download'] == True or os.path.exists(positive_records_file) == False or os.path.exists(negative_records_file) == False:
                log('Labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))
                download_file(input_data_file_set['base_url'] +  input_data_file_set['positive_records_file'], positive_records_file)
                download_file(input_data_file_set['base_url'] +  input_data_file_set['negative_records_file'], negative_records_file)
        
            log('Positive records file: {}'.format(os.path.basename(positive_records_file)))
            log('Negative records file: {}'.format(os.path.basename(negative_records_file)))
        
            log('Building positive features...')
            positive_file_features += build_labeled_features(positive_records_file, 'pos', ignore_duplicate_training_records, record_hash_dict,  duplicate_check_ignore_pattern, False, labeled_files_max_num_records_to_read, all_pos_records_file)

            log('Building negative features...')
            negative_file_features += build_labeled_features(negative_records_file, 'neg', False, ignore_duplicate_training_records, record_hash_dict,  duplicate_check_ignore_pattern, labeled_files_max_num_records_to_read, all_neg_records_file)

        if max_num_labeled_records_to_use is not None and len(positive_file_features) > max_num_labeled_records_to_use:
            log('Randomly taking {} records from {} positive features records...'.format(max_num_labeled_records_to_use, len(positive_file_features)))
            random.shuffle(positive_file_features)
            positive_file_features = positive_file_features[:max_num_labeled_records_to_use]

        if max_num_labeled_records_to_use is not None and len(negative_file_features) > max_num_labeled_records_to_use:
            log('Randomly taking {} records from {} negative features records...'.format(max_num_labeled_records_to_use, len(negative_file_features)))
            random.shuffle(negative_file_features)
            negative_file_features = negative_file_features[:max_num_labeled_records_to_use]

        total_positive_records_count = len(positive_file_features)
        if len(positive_file_features) < len(negative_file_features):
            log('Randomly taking {} records from {} negative features records to match the number of positive records...'.format(total_positive_records_count, len(negative_file_features)))
            random.shuffle(negative_file_features)
            negative_file_features = negative_file_features[:total_positive_records_count]

        all_pos_records_file.close()
        all_neg_records_file.close()

        training_set_cut_off_positive = int(len(positive_file_features) * .75)
        training_set_cut_off_negative = int(len(negative_file_features) * .75)

        training_featureset = positive_file_features[:training_set_cut_off_positive] + negative_file_features[:training_set_cut_off_negative]
        testing_featureset = positive_file_features[training_set_cut_off_positive:] + negative_file_features[training_set_cut_off_negative:]
        log('Model will be trained on {} and tested on {} featureset instances. Training the model now (this may take a while)...'.format(len(training_featureset), len(testing_featureset)))


        if 'naive_bayes_bow' in model_name:
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
                uploader.upload_files([pickle_file, all_pos_records_file_path, all_neg_records_file_path], output_dir, os.path.join(output_dir, model_archive_name))


        model_end_time = datetime.datetime.now()
        log('Completed creating model for: {} at {}. Duration: {}...'.format(model_name, model_end_time, model_end_time - model_start_time))


    end_time = datetime.datetime.now()
    log('modeler::create_models() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
    log('Uploading (best effort) logs now...')
    __log_file_handle.close()

    if config.upload_output_to_cloud == True:
        uploader.upload_files([log_file_path], output_dir, os.path.join(output_dir, 'log_{}.zip'.format(end_time.strftime("%Y%m%d-%H%M%S"))))

def build_labeled_features(file, label, skip_duplicates, record_hash_dict, duplicate_check_ignore_pattern, skip_first_record=False, max_records = None, output_file=None):
    log('Building ({}) features for file {}...'.format(label, file))
    file_features = []
    file_base_name = os.path.basename(file)
    total_records = 0
    total_data_records = 0
    fin = codecs.open(file, encoding='utf-8', errors='ignore')
    for record in fin:
        if len(record.strip()) == 0:
            continue

        total_records += 1
        sys.stdout.write('{} => Now processing record: {}...\r'.format(file_base_name, total_records))
        sys.stdout.flush()

        if total_records == 1 and skip_first_record == True:
            continue

        if skip_duplicates == True and record_hash_dict is not None:
            if config.verbose == True:
                log('Checking if this record is a duplicate...')

            record_to_hash = None
            if duplicate_check_ignore_pattern is not None:
                record_to_hash = duplicate_check_ignore_pattern.sub('', record)
            else:
                record_to_hash = record

            if config.verbose == True:
                log('Creating a SHA1 hash of this: {}'.format(record_to_hash))


            record_hash = hashlib.sha1(record_to_hash.upper().encode(errors='ignore')).hexdigest()
            record_id = record[:40]

            if config.verbose == True:
                log('Hash for this record ({}...) is: {}'.format(record_id, record_hash))


            if record_hash in record_hash_dict:
                log('DUPLICATE - Record {} is a duplicate of {}. It will be ignored'.format(record_id, record_hash_dict[record_hash]))
                continue

            if config.verbose == True:
                log('Hash does not already exist, which means this is not a duplicate record.'.format(record_id, record_hash))

            record_hash_dict[record_hash] = record_id

        if output_file is not None:
            output_file.write(record)

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
