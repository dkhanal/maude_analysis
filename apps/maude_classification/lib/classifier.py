# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import datetime
import codecs
import platform
import urllib
import logging

import nltk
import numpy

from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier

import sharedlib
import config

def extract_features(model_name, list_of_words):
    features = {}

    if 'bow' in model_name:
        for w in list_of_words:
            features[w] = True
    elif 'bigram' in model_name:
        for bigram in nltk.bigrams(list_of_words):
            features[bigram] = True
    elif 'trigram' in model_name:
        for trigram in nltk.ngrams(list_of_words, 3):
            features[trigram] = True

    return features

def classify_files(files_to_classify):
    output_dir = sharedlib.abspath(config.output_dir)
    models_dir = sharedlib.abspath(config.models_dir)

    start_time = datetime.datetime.now()
    process_log_first_line = 'MAUDE Classification Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    log(process_log_first_line)
    log('classifier::classify_files() starting at {}'.format(start_time))

    models_config = config.models
    models = []
    log('Checking if model(s) need to be downloaded...')

    models_on_remote_server = sharedlib.get_list_of_files_from_remote_server(config.remote_server['models_dir'])
    for model_config in models_config:
        model_name = model_config['name'] 
        classifier_pickle_file = os.path.join(models_dir, model_name + '.pickle')
        vectorizer_pickle_file = os.path.join(models_dir, model_name + '.vectorizer.pickle')
        if model_config['always_download'] == True or os.path.exists(classifier_pickle_file) == False:
            log('Model {} needs to be downloaded.'.format(model_name))

            if not model_config['archive_name'] in models_on_remote_server:
                log('Model archive {} not found on the remote server. This model will be skipped.'.format(model_config['archive_name']))
                continue

            download_zip_file_path = os.path.join(models_dir, model_config['archive_name'])

            model_url = sharedlib.join_remote_server_paths(config.remote_server['base_uri'], config.remote_server['models_dir'], model_config['archive_name'])

            sharedlib.download_file(model_url, download_zip_file_path)
            log('Extracting model archive...')
            sharedlib.unzip(download_zip_file_path, models_dir)
            log('Model extracted.')
        
        log('Classifier pickle file: {}'.format(os.path.basename(classifier_pickle_file)))
        log('Loading the pickled classifier...')
        classifier = sharedlib.load_pickle(classifier_pickle_file)
        vectorizer = None

        if os.path.exists(vectorizer_pickle_file):
            log('Vectorizer pickle file: {}'.format(os.path.basename(vectorizer_pickle_file)))
            log('Loading the pickled vectorizer...')
            vectorizer = sharedlib.load_pickle(vectorizer_pickle_file)
        else:
            log('No vectorizer (expected: {}) found for this model.'.format(vectorizer_pickle_file))


        log('Model ({}) loaded.'.format(classifier))
        models.append((model_name, classifier, vectorizer))
       
    log('Total {} model(s) loaded.'.format(len(models)))
    for input_data_file in files_to_classify:
        classify_file(input_data_file, models, True, config.target_file_max_num_records_to_classify)

    end_time = datetime.datetime.now()
    log('classifier::classify_files() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

def classify_record(record, models):
    results = []
    for (name, classifier, vectorizer) in models:
        results.append((name, classify(record, name, classifier, vectorizer)))

    return results


def classify(record, model_name, classifier, vectorizer):
    predicted_classification = None
    positive_probability = None
    if 'nltk.' in model_name:
        record_lower_case = record.lower()
        record_words = word_tokenize(record_lower_case)
        record_features = extract_features(model_name, record_words)

        predicted_classification = classifier.classify(record_features)
        probabilities = classifier.prob_classify(record_features)
        positive_probability = probabilities.prob('pos')
    elif 'sklearn.' in model_name:
        x_counts = vectorizer.transform([record])
        tf_transformer = TfidfTransformer(use_idf=False)
        x_tfidf = tf_transformer.transform(x_counts)

        predicted_classification = classifier.predict(x_tfidf)[0]
        probabilities = classifier.predict_proba(x_tfidf)
        positive_probability = probabilities[0][numpy.where(classifier.classes_ == 'pos')][0]
    else:
        raise ValueError('Unrecognized model name.')

    return (predicted_classification, positive_probability)

def get_overall_classification(classifications):
    if classifications is None or len(classifications) == 0:
        return None

    total_classifications = len(classifications)
    positive_classifications = len([s for s in classifications if 'pos' in s.lower()])
    negative_classifications = len([s for s in classifications if 'neg' in s.lower()])
    positive_prob = positive_classifications/total_classifications

    if  positive_classifications >= total_classifications/2:
        return ('pos', positive_prob)

    if negative_classifications >= total_classifications/2:
        return ('neg', positive_prob) # The probability returned is always for positive classification

    return None

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1
    return line_count

def show_model_classification_stats(file_name, model_name, positive_records_file, negative_records_file):
    all_positive_count = get_total_lines_count(positive_records_file)
    all_negative_count = get_total_lines_count(negative_records_file)
    all_total = all_positive_count + all_negative_count

    log('Model ({}), Stats for File: {}: Total: {}, POS: {}/{:.2f}%, NEG: {}/{:.2f}%'.format(model_name, file_name, all_total, all_positive_count, (all_positive_count/all_total * 100), all_negative_count, (all_negative_count/all_total * 100)))



def classify_file(input_data_file, models, skip_first_record=True, max_records = None):
    start_time = datetime.datetime.now()
    log('classifier::classify_file() starting at {}'.format(start_time))

    file_base_name = os.path.basename(input_data_file)
    out_dir = sharedlib.abspath(config.output_dir)
    predicted_pos_file_ext = '.predicted.pos.txt'
    predicted_neg_file_ext = '.predicted.neg.txt'
    prediction_summary_file_ext = '.prediction.summary.txt'

    overall_predicted_pos_records_file_path = os.path.join(out_dir, '{}{}'.format(file_base_name, predicted_pos_file_ext))
    overall_predicted_neg_records_file_path = os.path.join(out_dir, '{}{}'.format(file_base_name, predicted_neg_file_ext))
    prediction_summary_file_path = os.path.join(out_dir, '{}{}'.format(file_base_name, prediction_summary_file_ext))
    log('Predicted positive records file (overall): {}'.format(overall_predicted_pos_records_file_path))
    log('Predicted negative records file (overall): {}'.format(overall_predicted_neg_records_file_path))
    log('Prediction summary file: {}'.format(prediction_summary_file_path))

    prediction_summary_file =  open(prediction_summary_file_path, 'w', encoding='utf-8', errors='ignore')
    prediction_summary_file.write('RECORD_ID\tMODEL_NAME\tPOS_PROB\tNEG_PROB\tCLASSIFICATION\n')

    classifiers_info = []
    for (name, classifier, vectorizer) in models:
        log('Building classifier parameters for {}...'.format(name))
        predicted_positive_records_file_path = os.path.join(out_dir, '{}_{}{}'.format(file_base_name, name, predicted_pos_file_ext))
        predicted_negative_records_file_path = os.path.join(out_dir, '{}_{}{}'.format(file_base_name, name, predicted_neg_file_ext))
        log('Predicted positive records file for this classifier: {}'.format(predicted_positive_records_file_path))
        log('Predicted negative records file for this classifier: {}'.format(predicted_negative_records_file_path))
        classifiers_info.append((name, 
                                 classifier, 
                                 vectorizer,
                                 predicted_positive_records_file_path, 
                                 open(predicted_positive_records_file_path, 'w', encoding='utf-8', errors='ignore'), 
                                 predicted_negative_records_file_path, 
                                 open(predicted_negative_records_file_path, 'w', encoding='utf-8', errors='ignore')))

    unknown_records_file = sharedlib.abspath(input_data_file)
    log('Total {} models loaded.'.format(len(classifiers_info)))
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
    fin = codecs.open(unknown_records_file, mode='r+', encoding='utf-8', errors='ignore')
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

        classifications = []
        for (name, classifier, vectorizer, pos_file_path, pos_file, neg_file_path, neg_file) in classifiers_info:

            predicted_classification, positive_probability = classify(record, name, classifier, vectorizer)

            is_positive = predicted_classification == 'pos' and positive_probability > config.positive_probability_threshold

            if config.verbose == True:
                log('Classification by {} is {}'.format(name, predicted_classification))
                log('Probabilities: pos: {}, neg: {}'.format(positive_probability, probabilities.prob('neg')))
    
            if is_positive:
                classifications.append('pos')
                pos_file.write(record)
            else:
                classifications.append('neg')
                neg_file.write(record)

            prediction_summary_file.write('{}\t{}\t{:.2f}\t{:.2f}\t{}\n'.format(record[:40].strip(), name, positive_probability, 1-positive_probability, 'pos' if is_positive == True else 'neg', ))

            if total_data_records % 10000 == 0:
                pos_file.flush()
                neg_file.flush()
                prediction_summary_file.flush()
                show_model_classification_stats(file_base_name, name, pos_file_path, neg_file_path)

        overall_classification, overall_positive_probability = get_overall_classification(classifications)
        if overall_classification is None:
            continue

        if overall_classification == 'pos':
            overall_predicted_pos_records_file.write(record)
            total_positive +=1
        else:
            overall_predicted_neg_records_file.write(record)
            total_negative +=1

        prediction_summary_file.write('{}\t{}\t{:.2f}\t{:.2f}\t{}\n'.format(record[:40].strip(), 'overall',  overall_positive_probability, 1-overall_positive_probability, overall_classification))

        positive_percent = (total_positive / total_data_records) * 100
        negative_percent = (total_negative / total_data_records) * 100

    log('{}=> Overall {} POS records in total {} ({:.2f}%) with a probability of {} or higher.'.format(file_base_name, total_positive, total_data_records, positive_percent, config.positive_probability_threshold))    
    fin.close()

    log('Closing output files...')
    overall_predicted_pos_records_file.close()
    overall_predicted_neg_records_file.close()
    prediction_summary_file.close()

    files_to_zip = []
    for (name, classifier, pos_file_path, pos_file_handle, neg_file_path, neg_file_handle) in classifiers_info:
        files_to_zip.append(pos_file_path)
        if config.upload_positive_files_only == False:
            files_to_zip.append(neg_file_path)
        if config.verbose == True:
            log('Closing {}...'.format(pos_file_path))
        pos_file_handle.close()
    
        if config.verbose == True:
            log('Closing {}...'.format(neg_file_path))
        neg_file_handle.close()
        show_model_classification_stats(file_base_name, name, pos_file_path, neg_file_path)

    files_to_zip.append(prediction_summary_file_path)
    files_to_zip.append(overall_predicted_pos_records_file_path)
    if config.upload_positive_files_only == False:
        files_to_zip.append(overall_predicted_neg_records_file_path)

    if config.upload_output_to_remote_server == True:
        archive_name = os.path.splitext(file_base_name)[0]+'.zip'
        zip_file = sharedlib.zip_files(files_to_zip, os.path.join(out_dir, archive_name))
        log('Uploading the output files ({}) to the Remote Server...'.format(archive_name))
        sharedlib.upload_files_to_classification_dir([zip_file])

    end_time = datetime.datetime.now()
    log('classifier::classify_file() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


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
    logging.info(line)