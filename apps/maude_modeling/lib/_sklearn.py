import numpy
import sys
import os
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
import logging

import nltk
from nltk import word_tokenize

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def get_records(files_to_read):
    for filename, max_records_to_read in files_to_read:
        record_count = 0
        with open(filename) as f:
            for line in f:
                record_count += 1
                if max_records_to_read is not None and record_count > max_records_to_read:
                    break  

                yield line

def generate_model(positive_records_file, negative_records_file, model_config, output_dir):
    model_name = model_config['name']
    logging.info('Generating model {}...'.format(model_name))
    labeled_files_max_num_records_to_read = model_config['labeled_files_max_num_records_to_read']
    max_num_labeled_records_to_use = model_config['max_num_labeled_records_to_use']
    use_equal_positive_and_negative_labeled_records = model_config['use_equal_positive_and_negative_labeled_records']

    positive_file_total_records = get_total_lines_count(positive_records_file)
    negative_file_total_records = get_total_lines_count(negative_records_file)

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


    labels = (['pos'] * total_positive_records_to_read) + (['neg'] * total_negative_records_to_read)
    length_of_labels = len(labels)
    logging.info('Length of labels is {}. {} \'pos\' and {} \'neg\''.format(length_of_labels, length_of_labels/2, length_of_labels/2))

    vectorizer = CountVectorizer(input='content')

    x_train = vectorizer.fit_transform(get_records([(positive_records_file, total_positive_records_to_read), (negative_records_file, total_negative_records_to_read)]))
    tf_transformer = TfidfTransformer(use_idf=False).fit(x_train)
    x_train_tf = tf_transformer.transform(x_train)

    classifier = None
    if 'sgd' in model_name:
        classifier = SGDClassifier(loss='log').fit(x_train_tf, labels)
    elif 'voting' in model_name:
        lrc = LogisticRegression(random_state=1)
        mnbc = MultinomialNB()
        vc = VotingClassifier(estimators=[('lr', lrc), ('mnb', mnbc)], voting='soft')
        classifier = vc.fit(x_train_tf, labels)
    else:
        raise ValueError('Unsupported model: {}'.format(model_name))

    logging.info('Classifier shape: {}'.format(x_train_tf.shape))

    return classifier, vectorizer
