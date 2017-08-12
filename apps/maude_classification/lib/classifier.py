import os
import sys
import datetime
import pickle
import codecs
import platform
import urllib

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

def classify(input_data_files):
    output_dir = util.fix_path(config.output_dir)
    models_dir = util.fix_path(config.models_dir)
    log_file_path = os.path.join(output_dir, 'process.log')

    global __log_file_handle
    __log_file_handle = open(log_file_path, 'w')

    start_time = datetime.datetime.now()
    process_log_first_line = 'MAUDE Classification Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    log(process_log_first_line)
    log('classifier::classify_files() starting at {}'.format(start_time))

    models_config = config.models
    models = []
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
        log('Loading the pickled model...')
        model = util.load_pickle(model_pickle_file)
        log('Model ({}) loaded.'.format(model))
        models.append((model_name, model))
       
    log('Total {} model(s) loaded.'.format(len(models)))
    for input_data_file in input_data_files:
        classify_file(input_data_file, models, True, config.target_file_max_num_records_to_classify)

    end_time = datetime.datetime.now()
    log('classifier::classify_files() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
    log('Uploading (best effort) logs now...')
    __log_file_handle.close()

    if config.upload_output_to_cloud == True:
        uploader.upload_files([log_file_path], output_dir, os.path.join(output_dir, 'log_{}.zip'.format(end_time.strftime("%Y%m%d-%H%M%S"))))

def classify_file(input_data_file, models, skip_first_record=True, max_records = None):
    start_time = datetime.datetime.now()
    log('classifier::classify_file() starting at {}'.format(start_time))

    file_base_name = os.path.basename(input_data_file)
    out_dir = util.fix_path(config.output_dir)
    predicted_pos_file_ext = '.predicted.pos.txt'
    predicted_neg_file_ext = '.predicted.neg.txt'

    overall_predicted_pos_records_file_path = os.path.join(out_dir, '{}{}'.format(file_base_name, predicted_pos_file_ext))
    overall_predicted_neg_records_file_path = os.path.join(out_dir, '{}{}'.format(file_base_name, predicted_neg_file_ext))
    log('Predicted positive records file (overall): {}'.format(overall_predicted_pos_records_file_path))
    log('Predicted negative records file (overall): {}'.format(overall_predicted_neg_records_file_path))

    classifiers_info = []
    for (name, classifier) in models:
        log('Building classifier parameters for {}...'.format(name))
        predicted_positive_records_file_path = os.path.join(out_dir, '{}_{}{}'.format(file_base_name, name, predicted_pos_file_ext))
        predicted_negative_records_file_path = os.path.join(out_dir, '{}_{}{}'.format(file_base_name, name, predicted_neg_file_ext))
        log('Predicted positive records file for this classifier: {}'.format(predicted_positive_records_file_path))
        log('Predicted negative records file for this classifier: {}'.format(predicted_negative_records_file_path))
        classifiers_info.append((name, 
                                 classifier, 
                                 predicted_positive_records_file_path, 
                                 open(predicted_positive_records_file_path, 'w', encoding='utf-8', errors='ignore'), 
                                 predicted_negative_records_file_path, 
                                 open(predicted_negative_records_file_path, 'w', encoding='utf-8', errors='ignore')))

    unknown_records_file = util.fix_path(input_data_file)
    log('Unknown records file: {}'.format(unknown_records_file))
    log('Reading the unknown records file. One record at a time.'.format(classifier))

    total_records = 0
    total_data_records = 0
    total_positive = 0
    total_negative = 0
    positive_percent = 0
    negative_percent = 0
    
    overall_predicted_pos_records_file = open(overall_predicted_pos_records_file_path, 'w', encoding='utf-8', errors='ignore')
    overall_predicted_neg_records_file = open(overall_predicted_neg_records_file_path, 'w', encoding='utf-8', errors='ignore')
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

        positive_per_at_least_one_classifier = False
        negative_per_at_least_one_classifier = False

        for (name, classifier, pos_file_path, pos_file, neg_file_path, neg_file) in classifiers_info:
            predicted_classification = classifier.classify(record_features)

            probabilities = classifier.prob_classify(record_features)
            positive_probability = probabilities.prob('pos')

            is_positive = predicted_classification == 'pos' and positive_probability > config.positive_probability_threshold

            if config.verbose == True:
                log('Classification by {} is {}'.format(name, predicted_classification))
                log('Probabilities: pos: {}, neg: {}'.format(positive_probability, probabilities.prob(config.tag_negative)))
    
            if is_positive:
                total_positive +=1
                pos_file.write(record)
                if positive_per_at_least_one_classifier == False:
                    overall_predicted_pos_records_file.write(record)
                    positive_per_at_least_one_classifier = True
            else:
                total_negative +=1
                neg_file.write(record)
                if negative_per_at_least_one_classifier == False:
                    overall_predicted_neg_records_file.write(record)
                    negative_per_at_least_one_classifier = True

            positive_percent = (total_positive / total_data_records) * 100
            negative_percent = (total_negative / total_data_records) * 100


    log('{}=> {} POS records in total {} ({:.2f}%) with a probability of {} or higher.'.format(file_base_name, total_positive, total_data_records, positive_percent, config.positive_probability_threshold))    
    fin.close()

    log('Closing output files...')
    overall_predicted_pos_records_file.close()
    overall_predicted_neg_records_file.close()

    files_to_zip = []
    for (name, classifier, pos_file_path, pos_file_handle, neg_file_path, neg_file_handle) in classifiers_info:
        files_to_zip.append(pos_file_path)
        if config.upload_positive_files_only == False:
            files_to_zip.append(neg_file_path)
        log('Closing {}...'.format(pos_file_path))
        pos_file_handle.close()
        log('Closing {}...'.format(neg_file_path))
        neg_file_handle.close()

    files_to_zip.append(overall_predicted_pos_records_file_path)
    if config.upload_positive_files_only == False:
        files_to_zip.append(overall_predicted_neg_records_file_path)

    if config.upload_output_to_cloud == True:
        archive_name = os.path.splitext(file_base_name)[0]+'.zip'
        log('Uploading the output files ({}) to the Cloud...'.format(archive_name))
        uploader.upload_files(files_to_zip, out_dir, os.path.join(out_dir, archive_name))


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
    print(line)
