import numpy
import sys
import os
import time
import string

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import text
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import logging

import nltk
from nltk import word_tokenize

import sharedlib
import config

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def dump_2d_array_to_log(ar):
    logging.info('[')
    for row in ar:
        row_str = '['
        for element in row:
            row_str += '{},'.format(element)
        
        row_str = row_str.rstrip(',')
        row_str += ']'
        logging.info(row_str)
    logging.info(']')

def dump_1d_array_to_log(ar):
    row_str = '['
    for element in ar:
        row_str += '{},'.format(element)        
    row_str = row_str.rstrip(',')
    logging.info(row_str + ']')

def get_records(files_to_read):
    for filename, begin, max_records_to_read in files_to_read:
        records_count = 0
        records_read = 0
        with open(filename) as f:
            for line in f:
                records_count += 1
                if begin is not None and records_count <= begin: # begin is zero-based
                    continue; # Skip until the begin record is reached
                     
                if max_records_to_read is not None and records_read >= max_records_to_read:
                    break  

                records_read += 1
                yield line


def log_most_informative_features(classifier, vectorizer, n):

    if vectorizer is None:
        return

    feature_names = vectorizer.vocabulary_    
    logging.info('All ({}) items in vocabulary: '.format(len(feature_names)))
    for feature_name in feature_names:
        logging.info(feature_name)


    # Not all classifiers have coefficients (e.g. Voting Classifier does not)
    if classifier is None:
        return

    classifiers = None

    # Check if the classifier is a voting one or standalone
    if hasattr(classifier, 'coef_'):
        classifiers = [classifier]
    elif hasattr(classifier, 'estimators_'):
        classifiers = classifier.estimators_

    if classifiers is None:
        return
    
    feature_names = vectorizer.get_feature_names()    
    for obj in classifiers:
        name = str(obj)
        if not hasattr(obj, 'coef_'):
           logging.info('No coef_ in model: '.format(name))
           continue

        logging.info('Most informative features for classifier ({}): '.format(name))

        # Build flattened list in lower coefficient to higher order
        feature_coefficents = sorted(zip(obj.coef_[0], feature_names))
    
        # Build two lists of same size -- one from the head of the list, another tail
        topN = zip(feature_coefficents[:n], feature_coefficents[:-(n + 1):-1])
    
        for (c1, feature1), (c2, feature2) in topN:
            logging.info("\t{:.2f}\t{}\t\t\t{:.2f}\t{}".format(c1, feature1, c2, feature2))


def generate_model(positive_records_file, negative_records_file, model_config, output_dir):
    model_name = model_config['name']
    logging.info('Generating model {}...'.format(model_name))
    tmp_positive_records_file = positive_records_file + '.tmp'
    tmp_negative_records_file = negative_records_file + '.tmp'

    sharedlib.copy_file(positive_records_file, tmp_positive_records_file)
    sharedlib.copy_file(negative_records_file, tmp_negative_records_file)

    logging.info('Randomizing records in {}...'.format(tmp_positive_records_file))
    sharedlib.randomize_records(tmp_positive_records_file)

    logging.info('Randomizing records in {}...'.format(tmp_negative_records_file))
    sharedlib.randomize_records(tmp_negative_records_file)

    labeled_files_max_num_records_to_read = model_config['labeled_files_max_num_records_to_read']
    max_num_labeled_records_to_use = model_config['max_num_labeled_records_to_use']
    use_equal_positive_and_negative_labeled_records = model_config['use_equal_positive_and_negative_labeled_records']

    positive_file_total_records = get_total_lines_count(tmp_positive_records_file)
    negative_file_total_records = get_total_lines_count(tmp_negative_records_file)

    total_positive_records_to_read = positive_file_total_records
    total_negative_records_to_read = negative_file_total_records

    if use_equal_positive_and_negative_labeled_records == True:
        total_records_to_read = min(positive_file_total_records, negative_file_total_records)
        total_positive_records_to_read = total_records_to_read
        total_negative_records_to_read = total_records_to_read


    if labeled_files_max_num_records_to_read is not None:
       if labeled_files_max_num_records_to_read < total_positive_records_to_read:
           total_positive_records_to_read = labeled_files_max_num_records_to_read

       if labeled_files_max_num_records_to_read < total_negative_records_to_read:
           total_negative_records_to_read = labeled_files_max_num_records_to_read


    training_set_cut_off_positive = int(total_positive_records_to_read * .75)
    training_set_cut_off_negative = int(total_negative_records_to_read * .75)

    testing_set_cut_off_positive = total_positive_records_to_read - training_set_cut_off_positive
    testing_set_cut_off_negative = total_negative_records_to_read - training_set_cut_off_negative

    logging.info('Total labeled records {} positive and {} negative.'.format(total_positive_records_to_read, total_negative_records_to_read))

    train_labels = (['pos'] * training_set_cut_off_positive) + (['neg'] * training_set_cut_off_negative)
    length_of_train_labels = len(train_labels)
    logging.info('Length of train_labels is {}. {} \'pos\' and {} \'neg\''.format(length_of_train_labels, training_set_cut_off_positive, training_set_cut_off_negative))

    test_labels = (['pos'] * testing_set_cut_off_positive) + (['neg'] * testing_set_cut_off_negative)
    length_of_test_labels = len(test_labels)
    logging.info('Length of test_labels is {}. {} \'pos\' and {} \'neg\''.format(length_of_test_labels, testing_set_cut_off_positive, testing_set_cut_off_negative))

    stop_words = text.ENGLISH_STOP_WORDS
    if config.custom_stop_words is not None:
        stop_words = stop_words.union([sw.lower() for sw in config.custom_stop_words])

    stop_words = sorted(stop_words)
    logging.info('These stop words will be omitted from the records')
    for sw  in stop_words:
        logging.info(sw)

    vectorizer = CountVectorizer(input ='content', 
                                 encoding = 'utf-8',
                                 min_df =.001, 
                                 stop_words = stop_words,
                                 lowercase = True)

    x_train = vectorizer.fit_transform(get_records([(tmp_positive_records_file, 0, training_set_cut_off_positive), (tmp_negative_records_file, 0, training_set_cut_off_negative)]))
    logging.info('CountVectorizer - Fitted matrix shape: {}'.format(x_train.shape))
    features = vectorizer.get_feature_names()
    logging.info('CountVectorizer - Features (Total: {}):'.format(len(features)))
    dump_1d_array_to_log(features)

    tfidf_transformer = TfidfTransformer(use_idf=True, norm='l2').fit(x_train)
    x_train_tf = tfidf_transformer.transform(x_train)

    classifier = None
    if 'sgd' in model_name:
        classifier = SGDClassifier(loss='hinge', penalty ='l2',alpha = 0.0001).fit(x_train_tf, train_labels)
    elif 'mnb' in model_name:
        classifier = MultinomialNB()
    elif 'logreg' in model_name:
        classifier = LogisticRegression(random_state = 1)
    else:
        raise ValueError('Unsupported model: {}'.format(model_name))

    classifier.fit(x_train_tf, train_labels)
    logging.info('Classifier shape: {}'.format(x_train_tf.shape))
    logging.info('Testing the classifier now...')

    x_test = vectorizer.transform(get_records([(tmp_positive_records_file, training_set_cut_off_positive, testing_set_cut_off_positive), (tmp_negative_records_file, training_set_cut_off_negative, testing_set_cut_off_negative)]))
    tfidf_transformer_test = TfidfTransformer(use_idf=True, norm='l2').fit(x_test)
    x_test_tf = tfidf_transformer_test.transform(x_test)
    score = classifier.score(x_test_tf, test_labels)    
    logging.info('Classifier score: {}'.format(score))

    log_most_informative_features(classifier, vectorizer, 500)

    sharedlib.delete_file(tmp_positive_records_file)
    sharedlib.delete_file(tmp_negative_records_file)
    
    return classifier, vectorizer, score
