import os
import sys
import datetime
import pickle
import codecs

import nltk
from nltk import word_tokenize

import config
import util

def extract_features(list_of_words):
    features = {}
    for w in list_of_words:
        features[w] = True
    
    return features

def classify(input_data_files):
    output_dir = util.fix_path(config.output_dir)
    models_dir = util.fix_path(config.models_dir)
    log_file_path = os.path.join(output_dir, 'process.log')

    global __log_file_handle
    __log_file_handle = open(log_file_path, 'w')

    start_time = datetime.datetime.now()
    log('classifier::classify_files() starting at {}'.format(start_time))

    input_data_file_sets = config.input_data_file_sets
    models_config = config.model

    log('Checking if model(s) need to be downloaded...')
    for model_config in models_config:
        model_name = model_config['name'] 
        model_pickle_file = os.path.join(models_dir, model_name + '.pickle')
        if model_config['always_download'] == True or os.path.exists(model_pickle_file) == False:
            log('Model {} needs to be downloaded.'.format(model_name))
            download_zip_file_path = os.path.join(models_dir, model_name + '.zip')
            download_file(model_config['remote_url'], download_zip_file_path)
            log('Extracting model archive...')
            util.unzip(download_zip_file_path, models_dir)
            log('Model extracted.')
        
        log('Model pickle file: {}'.format(os.path.basename(model_pickle_file)))
        
    for input_data_file in input_data_files:
        for model_config in models_config:
            classify_file(input_data_file, model_config, model_pickle_file, True, config.target_file_max_num_records_to_classify)

    end_time = datetime.datetime.now()
    log('classifier::classify_files() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
    log('Uploading (best effort) logs now...')
    __log_file_handle.close()

    if config.upload_output_to_cloud == True:
        uploader.upload_files([log_file_path], output_dir, os.path.join(output_dir, 'log_{}.zip'.format(end_time.strftime("%Y%m%d-%H%M%S"))))

def classify_file(input_data_file, model_config, model_pickle_file, skip_first_record=True, max_records = None):
    start_time = datetime.datetime.now()
    log('classifier::classify_file() starting at {}'.format(start_time))

    model_name = model_config['name']
    pickle_file = util.fix_path(model_pickle_file)
    unknown_records_file = util.fix_path(input_data_file)
    predicted_positive_records_file = util.fix_path(os.path.join(config.output_dir, model_name + '.predicted.pos.txt'))
    predicted_negative_records_file = util.fix_path(os.path.join(config.output_dir, model_name + '.predicted.neg.txt'))

    log('Unknown records file: {}'.format(unknown_records_file))
    log('Pickle file: {}'.format(pickle_file))
    log('Predicted positive records file: {}'.format(predicted_positive_records_file))
    log('Predicted negative records file: {}'.format(predicted_negative_records_file))
   
    log('Loading the pickled model...')
    classifier = util.load_pickle(pickle_file)
    log('Classifier ({}) loaded. Reading the unknown records file. One record at a time.'.format(classifier))

    file_base_name = os.path.basename(unknown_records_file)
    total_records = 0
    total_data_records = 0
    total_positive = 0
    total_negative = 0
    positive_percent = 0
    negative_percent = 0
    
    positive_output_file = open(predicted_positive_records_file, 'w')
    negative_output_file = open(predicted_negative_records_file, 'w')
    fin = codecs.open(unknown_records_file, encoding='utf-8', errors='ignore')
    for record in fin:
        total_records += 1
        sys.stdout.write('{} => POS: {}/{:.2f}% NEG: {}/{:.2f}% . Next: {}...\r'.format(file_base_name, 
                                                                                                            total_positive, positive_percent, 
                                                                                                            total_negative, negative_percent, 
                                                                                                            total_data_records))
        sys.stdout.flush()

        if total_records == 1 and skip_first_record == True:
            continue
            
        total_data_records += 1

        if max_records is not None and total_data_records > max_records:
            break

        record_lower_case = record.lower()
        record_words = word_tokenize(record_lower_case)
        record_features = extract_features(record_words)

        predicted_classification = classifier.classify(record_features)

        probabilities = classifier.prob_classify(record_features)
        positive_probability = probabilities.prob('pos')

        is_positive = predicted_classification == 'pos' and positive_probability > config.positive_probability_threshold

        if config.verbose == True:
            log('Classification is {}'.format(predicted_classification))
            log('Probabilities: pos: {}, neg: {}'.format(positive_probability, probabilities.prob(config.tag_negative)))
    
        if is_positive:
            total_positive +=1
            positive_output_file.write(record)
        else:
            total_negative +=1
            negative_output_file.write(record)

        positive_percent = (total_positive / total_data_records) * 100
        negative_percent = (total_negative / total_data_records) * 100

    log('{}=> {} POS records in total {} ({:.2f}%) with a probability of {} or higher.'.format(file_base_name, total_positive, total_data_records, positive_percent, config.positive_probability_threshold))    
    fin.close()
    positive_output_file.close()
    negative_output_file.close()

    end_time = datetime.datetime.now()
    log('classifier::classify_file() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))




def build_labeled_features(file, label, skip_first_record=False, max_records = None):
    log('Building ({}) features for file {}...'.format(label, file))
    file_features = []
    file_base_name = os.path.basename(file)
    total_records = 0
    total_data_records = 0
    fin = codecs.open(unknown_records_file, encoding='utf-8', errors='ignore')
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
    log(line)
