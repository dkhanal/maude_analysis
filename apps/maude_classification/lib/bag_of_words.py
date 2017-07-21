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

def create_models():
    start_time = datetime.datetime.now()
    print('bag_of_words::create_models() starting at {}'.format(start_time))

    input_data_file_sets = config.input_data_file_sets
    classifiers_config = config.classifiers

    for input_data_file_set in input_data_file_sets:
        for classifier_config in classifiers_config:
            create_model(input_data_file_set, classifier_config)

    end_time = datetime.datetime.now()
    print('bag_of_words::create_models() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

def create_model(data_file_set, classifier_config):
    start_time = datetime.datetime.now()
    print('bag_of_words::create_model() for set {} starting at {}'.format(start_time, data_file_set['name']))
    positive_records_file = util.fix_path(data_file_set['positive_records'])
    negative_records_file = util.fix_path(data_file_set['negative_records'])

    pickle_file = util.fix_path(os.path.join(config.pickles_dir, classifier_config['name'] + '.pickle'))

    print('Positive records file: {}'.format(positive_records_file))
    print('Negative records file: {}'.format(negative_records_file))
    print('Pickle file: {}'.format(pickle_file))

    print('Building positive features...')
    positive_file_features = build_labeled_features(positive_records_file, 'pos', False, config.labeled_files_max_num_records_to_read)

    print('Building negative features...')
    negative_file_features = build_labeled_features(negative_records_file, 'neg', False, config.labeled_files_max_num_records_to_read)

    training_set_cut_off_positive = int(len(positive_file_features) * .75)
    training_set_cut_off_negative = int(len(negative_file_features) * .75)

    training_featureset = positive_file_features[:training_set_cut_off_positive] + negative_file_features[:training_set_cut_off_negative]
    testing_featureset = positive_file_features[training_set_cut_off_positive:] + negative_file_features[training_set_cut_off_negative:]

    print('Model will be trained on {} and tested on {} featureset instances. Training the model now...'.format(len(training_featureset), len(testing_featureset)))
    classifier = nltk.classify.NaiveBayesClassifier.train(training_featureset)

    print( 'Model trained. Assessing its accuracy now using the testing set... ')
    accuracy = nltk.classify.util.accuracy(classifier, testing_featureset)

    print( 'Model accuracy is: {}. '.format(accuracy))
    classifier.show_most_informative_features()


    print( 'Pickling the model as: {}...'.format(os.path.basename(pickle_file)))
    util.pickle_object(classifier, pickle_file)

    end_time = datetime.datetime.now()
    print('bag_of_words::create_model() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))



def classify():
    start_time = datetime.datetime.now()
    print('bag_of_words::classify_files() starting at {}'.format(start_time))

    input_data_file_sets = config.input_data_file_sets
    classifiers_config = config.classifiers

    for input_data_file_set in input_data_file_sets:
        for classifier_config in classifiers_config:
            classify_file(input_data_file_set, classifier_config, True, config.target_file_max_num_records_to_classify)

    end_time = datetime.datetime.now()
    print('bag_of_words::classify_files() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

def classify_file(data_file_set, classifier_config, skip_first_record=True, max_records = None):
    start_time = datetime.datetime.now()
    print('bag_of_words::classify_file() starting at {}'.format(start_time))

    classifier_name = classifier_config['name']
    pickle_file = util.fix_path(os.path.join(config.pickles_dir, classifier_name + '.pickle'))
    unknown_records_file = util.fix_path(data_file_set['unknown_records'])
    predicted_positive_records_file = util.fix_path(os.path.join(config.output_dir, classifier_name + '.predicted.pos.txt'))
    predicted_negative_records_file = util.fix_path(os.path.join(config.output_dir, classifier_name + '.predicted.neg.txt'))

    print('Unknown records file: {}'.format(unknown_records_file))
    print('Pickle file: {}'.format(pickle_file))
    print('Predicted positive records file: {}'.format(predicted_positive_records_file))
    print('Predicted negative records file: {}'.format(predicted_negative_records_file))

    classifier = None
    if config.use_pickeled_models_if_present == False or not os.path.isfile(pickle_file):
        create_model(data_file_set, classifier_config)
    
    print('Loading the pickled model...')
    classifier = util.load_pickle(pickle_file)
    print('Classifier ({}) loaded. Reading the unknown records file. One record at a time.'.format(classifier))

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
            print('Classification is {}'.format(predicted_classification))
            print('Probabilities: pos: {}, neg: {}'.format(positive_probability, probabilities.prob(config.tag_negative)))
    
        if is_positive:
            total_positive +=1
            positive_output_file.write(record)
        else:
            total_negative +=1
            negative_output_file.write(record)

        positive_percent = (total_positive / total_data_records) * 100
        negative_percent = (total_negative / total_data_records) * 100

    print('{}=> {} POS records in total {} ({:.2f}%) with a probability of {} or higher.'.format(file_base_name, total_positive, total_data_records, positive_percent, config.positive_probability_threshold))    
    fin.close()
    positive_output_file.close()
    negative_output_file.close()

    end_time = datetime.datetime.now()
    print('bag_of_words::classify_file() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))




def build_labeled_features(file, label, skip_first_record=False, max_records = None):
    print('Building ({}) features for file {}...'.format(label, file))
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
    print('{} => Total {} record(s) processed.'.format(file_base_name, total_data_records))
    return file_features