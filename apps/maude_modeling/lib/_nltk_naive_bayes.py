import os
import codecs
import logging
import string
import sys
import random

import nltk
from nltk import word_tokenize

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

def build_labeled_features(model_name, file, label, skip_first_record=False, max_records=None, output_file=None):
    logging.info('Building ({}) features for file {}...'.format(label, file))
    file_features = []
    file_base_name = os.path.basename(file)
    total_records = 0
    total_data_records = 0
    fin = open(file, encoding='utf-8', errors="ignore")
    for record in fin:
        if len(record.strip()) == 0:
            continue

        total_records += 1
        sys.stdout.write('{} => Now processing record: {}...\r'.format(file_base_name, total_records))
        sys.stdout.flush()

        if total_records == 1 and skip_first_record == True:
            continue

        if output_file is not None:
            output_file.write(record)

        total_data_records += 1

        if max_records is not None and total_data_records > max_records:
            break

        punc_removal_table = str.maketrans({punc: None for punc in string.punctuation})
        record_lower_case_no_punc = record.lower().translate(punc_removal_table)
        record_words = word_tokenize(record_lower_case_no_punc)
        record_features = extract_features(model_name, record_words)

        if label == None:
            file_features.append(record_features)
        else:
            file_features.append((record_features, label))

    fin.close()
    logging.info('{} => Total {} record(s) processed.'.format(file_base_name, total_data_records))
    return file_features


def generate_model(positive_records_file, negative_records_file, model_config, output_dir):
    model_name = model_config['name']
    labeled_files_max_num_records_to_read = model_config['labeled_files_max_num_records_to_read']
    max_num_labeled_records_to_use = model_config['max_num_labeled_records_to_use']
    use_equal_positive_and_negative_labeled_records = model_config['use_equal_positive_and_negative_labeled_records']

    logging.info('Building positive features...')
    positive_file_features = build_labeled_features(model_name, positive_records_file, 'pos', False, labeled_files_max_num_records_to_read)

    logging.info('Building negative features...')
    negative_file_features = build_labeled_features(model_name, negative_records_file, 'neg', False, labeled_files_max_num_records_to_read)

    if max_num_labeled_records_to_use is not None and len(positive_file_features) > max_num_labeled_records_to_use:
        logging.info('Randomly taking {} records from {} positive features records...'.format(max_num_labeled_records_to_use, len(positive_file_features)))
        random.shuffle(positive_file_features)
        positive_file_features = positive_file_features[:max_num_labeled_records_to_use]

    if max_num_labeled_records_to_use is not None and len(negative_file_features) > max_num_labeled_records_to_use:
        logging.info('Randomly taking {} records from {} negative features records...'.format(max_num_labeled_records_to_use, len(negative_file_features)))
        random.shuffle(negative_file_features)
        negative_file_features = negative_file_features[:max_num_labeled_records_to_use]

    total_positive_records_count = len(positive_file_features)
    total_negative_records_count = len(negative_file_features)

    if use_equal_positive_and_negative_labeled_records == True and total_positive_records_count < total_negative_records_count:
        logging.info('Randomly taking {} records from {} negative features records to match the number of positive records...'.format(total_positive_records_count, total_negative_records_count))
        random.shuffle(negative_file_features)
        negative_file_features = negative_file_features[:total_positive_records_count]

    if use_equal_positive_and_negative_labeled_records == True and total_negative_records_count < total_positive_records_count:
        logging.info('Randomly taking {} records from {} positive features records to match the number of negative records...'.format(total_negative_records_count, total_positive_records_count))
        random.shuffle(positive_file_features)
        positive_file_features = positive_file_features[:total_negative_records_count]

    logging.info('Total featuresets in this model: Positive featuresets: {} Negative featuresets: {}...'.format(len(positive_file_features), len(negative_file_features)))

    training_set_cut_off_positive = int(len(positive_file_features) * .75)
    training_set_cut_off_negative = int(len(negative_file_features) * .75)

    training_featureset = positive_file_features[:training_set_cut_off_positive] + negative_file_features[:training_set_cut_off_negative]
    testing_featureset = positive_file_features[training_set_cut_off_positive:] + negative_file_features[training_set_cut_off_negative:]
    logging.info('Model ({}) will be trained on {} and tested on {} featureset instances. Training the model now (this may take a while)...'.format(model_name, len(training_featureset), len(testing_featureset)))

    if 'naive_bayes' in model_name:
        logging.info('Classifier in training:  nltk.classify.NaiveBayesClassifier')
        classifier = nltk.classify.NaiveBayesClassifier.train(training_featureset)

        logging.info('Model trained. Assessing its accuracy now using the testing set... ')
        accuracy = nltk.classify.util.accuracy(classifier, testing_featureset)

        logging.info('Model accuracy is: {}. '.format(accuracy))
        classifier.show_most_informative_features()

    return (classifier, accuracy)
