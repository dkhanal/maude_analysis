# By Deepak Khanal
# dkhanal@gmail.com

import datetime
import os
import nltk
import pickle
import random
import data_access
import json
import util
import config
from nltk.corpus import stopwords
from nltk import word_tokenize
from foi_text import FoiTextRow
         
def build_features(list_of_words, features_definition):
    # Each feature item has name, words (stemmed) to match, 
    # and minimum number of matches required to satisfy.
    # name, words, min_matches_required
    # Incoming list_of_words is also assumed to be stemmed.

    features = {}

    for feature_config in features_definition:
        name = feature_config['name']
        words_stemmed = feature_config['words_stemmed']
        min_matches_required = feature_config['min_matches_required']

        unique_words = set(words_stemmed)

        match_count = 0
        for feature_word in unique_words:
            if feature_word in list_of_words:
                match_count += 1

        if match_count > min_matches_required:
            features[name] = True
        else:
            features[name] = False

    return features

def extract_most_common_words(list_of_words, max):
    print('Extracting most common up to {} words...'.format(max))
    print('There are total {} words in the list. Computing frequency distribution...'.format(len(list_of_words)))
    if list_of_words is None or  len(list_of_words) == 0:
        return []
    
    # list_of_words is stemmed, so we stem the noise words too
    stemmer = nltk.stem.PorterStemmer()
    stemmed_noise_words = [stemmer.stem(w) for w in config.noise_words]

    # Eliminate punctuations, 'words' with less than 3 letters, and noise words    
    list_of_words = [w for w in list_of_words if len(w) > 2 and not w in stemmed_noise_words]

    all_words_fd = nltk.FreqDist(list_of_words)
    return [w for (w, f) in all_words_fd.most_common(max)]

def remove_stopwords(list_of_words):
    stop_words = stopwords.words('english')
    return [word for word in list_of_words if len(word) > 1 and word.lower() not in stop_words]

def stem_words(list_of_words):
    stemmer = nltk.stem.PorterStemmer()
    return [stemmer.stem(w) for w in list_of_words]


def create_models():
    start_time = datetime.datetime.now()
    print('create_models() starting at {}'.format(start_time))

    data_files = config.data_files_for_featureset

    print('Known positive signals used for this experiment written to: {}'.format(config.output_files['known_positive_records_selection_terms']))
    util.dump_list_to_file(config.known_positive_records_selection_terms, config.output_files['known_positive_records_selection_terms'])

    print('Potential positive signals used for this experiment written to: {}'.format(config.output_files['potential_positive_records_selection_terms']))
    util.dump_list_to_file(config.potential_positive_records_selection_terms, config.output_files['potential_positive_records_selection_terms'])

    print('Obtaining up to {} known positive records...'.format(config.known_positive_records_limit))
    known_positive_records = data_access.get_known_positives(data_files, config.known_positive_records_limit)
    util.dump_list_to_file(known_positive_records, config.output_files['known_positive_records'])

    print('Obtaining up to {} known negative records...'.format(config.known_negative_records_limit))
    known_negative_records = data_access.get_known_negatives(data_files, config.known_negative_records_limit)
    util.dump_list_to_file(known_negative_records, config.output_files['known_negative_records'])

    print('Word-tokenizing positive records...')
    words_in_known_positive_records =  [word_tokenize(line) for line in known_positive_records]

    print('Word-tokenizing negative records...')
    words_in_known_negative_records =  [word_tokenize(line) for line in known_negative_records]

    stop_words = stopwords.words('english')

    print('Removing stopwords from positive words...')
    words_without_stopwords_in_known_positive_records = [remove_stopwords(sublist) for sublist in words_in_known_positive_records]
    util.dump_list_to_file(words_without_stopwords_in_known_positive_records, config.output_files['words_in_known_positive_records'])

    print('Removing stopwords from negative words...')
    words_without_stopwords_in_known_negative_records =  [remove_stopwords(sublist) for sublist in words_in_known_negative_records]
    util.dump_list_to_file(words_without_stopwords_in_known_negative_records, config.output_files['words_in_known_negative_records'])

    print('Stemming words...')
    stemmer = nltk.stem.PorterStemmer()
    stemmed_words_without_stopwords_in_known_positive_records = [stem_words(sublist) for sublist in words_without_stopwords_in_known_positive_records]
    stemmed_words_without_stopwords_in_known_negative_records = [stem_words(sublist) for sublist in words_without_stopwords_in_known_negative_records]

    if config.use_fixed_features == True:
        # For fixed model, the configuration has the structure
        # Here, we simply inject a property for stemmed words
        # to the existing object.
        print('Building feature configuration using fixed features.')
        features_definition = config.fixed_features
        for feature_config in features_definition:
            feature_config['words_stemmed'] = [stemmer.stem(w) for w in feature_config['words']]
    else:
        print('Building feature configuration using most common words from known positive records...')
        print('Obtaining up to {} most common words from positive records...'.format(config.most_common_words_limit))
        all_words_in_all_positive_records = [w for sublist in stemmed_words_without_stopwords_in_known_positive_records for w in sublist]
        most_common_words = extract_most_common_words(all_words_in_all_positive_records, config.most_common_words_limit)

        features_definition = []
        for word in most_common_words:
            feature_config = {}
            feature_config['name'] = word
            feature_config['words'] = [word]
            feature_config['words_stemmed'] = [word] # Word is already stemmed
            feature_config['min_matches_required'] = 1

            features_definition.append(feature_config)

    util.dump_list_to_file(json.dumps(features_definition, indent=4).split('\n'), config.output_files['features_definition'])

    print('Tagging known data sets...')
    known_positives_tagged = [(sublist, config.tag_positive) for sublist in stemmed_words_without_stopwords_in_known_positive_records]
    known_negatives_tagged = [(sublist, config.tag_negative) for sublist in stemmed_words_without_stopwords_in_known_negative_records]

    print('Building training set...')
    known_tagged = known_positives_tagged + known_negatives_tagged

    print('Building feature set..')
    featureset = [(build_features(list_of_words, features_definition), tag) for (list_of_words, tag) in known_tagged]
    random.shuffle(featureset)
  
    half_mark = len(featureset) // 2
    print('Half of featureset list is: {}'.format(half_mark))

    training_set = featureset[:half_mark]
    testing_set = featureset[half_mark:]

    print('Training Naive Bayes classifier...')
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print('Training Naive Bayes classifier accuracy is: {}'.format(nltk.classify.accuracy(classifier, testing_set)))
    classifier.show_most_informative_features(10)

    classifiers = [('nltk.NaiveBayesClassifier', classifier)]

    end_time = datetime.datetime.now()

    print('create_models() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

    return (classifiers, features_definition)

def classify(classifiers, features_definition, skip_first_line=True, max = None):
    start_time = datetime.datetime.now()
    print('classify() starting at {}'.format(start_time))

    data_files = config.data_files_for_classification
    for file in data_files:
        if not os.path.isabs(file):
            full_file_path = os.path.join(os.path.dirname(__file__), file)
        else:
            full_file_path = file
        for classifier in classifiers:
            classifier_name = classifier[0]
            classifier_obj = classifier[1]
            positive_record_ids = classify_file(full_file_path, classifier_name, classifier_obj, features_definition, skip_first_line)
            util.dump_list_to_file(positive_record_ids, config.output_files['predicted_positive_records'])

    end_time = datetime.datetime.now()
    print('classify() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


def classify_file(file_path, classifier_name, classifier, features_definition, skip_first_line=True):
    file_name =  os.path.basename(file_path)
    print ('Classifiying using {} each record in file {}...'.format(classifier_name, file_name))

    total_lines = 0
    positive_record_ids = []
    percent = None
    with open(file_path) as f:
        for line in f:
            total_lines += 1
            if total_lines == 1 and skip_first_line:
                continue
            if config.data_file_max_num_rows_to_classify != None and total_lines > config.data_file_max_num_rows_to_classify:
                break;

            row = FoiTextRow(line=line)
            positive_records_count = len(positive_record_ids)
            lines_so_far = total_lines -1
            percent = round(positive_records_count / lines_so_far * 100, 2)

            if config.verbose == True or total_lines % 10000 == 0: # Unless in verbose mode, we write progress every 10000th record
                print('{}=>, {} {} records in total {} ({}%) so far. Checking row (report key: {} text key {})...'.format(file_name, positive_records_count, config.tag_positive, lines_so_far, percent, row.mdr_report_key, row.mdr_text_key))

            if len(row.foi_text.strip()) < 50: # Insufficient size of narrative text
                continue

            line_to_classify = row.foi_text.upper()
            words_to_classify = word_tokenize(line_to_classify)
            
            words_to_classify_without_stopwords = remove_stopwords(words_to_classify)
            stemed_words_to_classify = stem_words(words_to_classify_without_stopwords)

            line_features = build_features(stemed_words_to_classify, features_definition)

            predicted_classification = classifier.classify(line_features)

            probabilities = classifier.prob_classify(line_features)
            positive_probability = probabilities.prob(config.tag_positive)

            is_positive = predicted_classification == config.tag_positive and positive_probability > config.positive_probability_threshold

            if config.verbose == True:
                print('Classification is {}'.format(line_tag))
                print('Probabilities: {}: {}, {}: {}'.format(config.tag_positive, positive_probability, config.tag_negative, probabilities.prob(config.tag_negative)))
    
            if is_positive:
                if config.output_positive_record_id_only:
                    positive_record_ids.append(row.mdr_report_key + '|' + row.mdr_text_key)
                else:
                    positive_record_ids.append(row.mdr_report_key + '|' + row.mdr_text_key + '|' + row.foi_text)

        print('{}=>, {} {} records in total {} ({}%) with a probability of {} or higher.'.format(file_name, len(positive_record_ids), config.tag_positive, total_lines, percent, config.positive_probability_threshold))
        return positive_record_ids

def pickle_models(classifiers):
    print('Saving models as pickles...')
    for item in classifiers:
        # Item 0 is the classifier name. Item 1 the classifier object.
        pickle_model(item[0], item[1])

def pickle_model(classifier_name, classifier_obj):
    pickle_dir = config.pickles_save_dir
    if not os.path.isabs(pickle_dir):
        pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)
        
    pickle_file_path = os.path.join(pickle_dir, classifier_name + '.model.pickle')

    print('Pickling classifier as: {}...'.format(os.path.basename(pickle_file_path)))
    f = open(pickle_file_path, 'wb')
    pickle.dump(classifier_obj, f)
    f.close()

def load_pickled_models():
    pickle_dir = config.pickles_save_dir
    if not os.path.isabs(pickle_dir):
        pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)

    print('Loading pickled models from: {}...'.format(pickle_dir))

    models = []
    for filename in os.listdir(pickle_dir):
        if filename.endswith('.model.pickle'): 
            print('Loading pickled model {}...'.format(filename))
            f = open(os.path.join(pickle_dir, filename), 'rb')
            classifier = pickle.load(f)
            f.close()

            item = (filename.replace('.model.pickle', ''), classifier)
            models.append(item)

    print('Total {} pickled model(s) loaded.'.format(len(models)))
    return models

def pickle_features_definition(features_definition):
    pickle_file = config.output_files['features_definition_pickle']
    if not os.path.isabs(pickle_file):
        pickle_dir = config.pickles_save_dir
        if not os.path.isabs(pickle_dir):
            pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)
        pickle_file = os.path.join(pickle_dir, pickle_file)


    print('Pickling features definition as: {}...'.format(os.path.basename(pickle_file)))
    f = open(pickle_file, 'wb')
    pickle.dump(features_definition, f)
    f.close()

def load_pickled_features_definition():
    pickle_file = config.output_files['features_definition_pickle']
    if not os.path.isabs(pickle_file):
        pickle_dir = config.pickles_save_dir
        if not os.path.isabs(pickle_dir):
            pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)
        pickle_file = os.path.join(pickle_dir, pickle_file)


    print('Loading pickled features definition from: {}...'.format(os.path.basename(pickle_file)))
    if not os.path.isfile(pickle_file):
        print ('Pickle file does not exist.')
        return []

    f = open(pickle_file, 'rb')
    features_definition = pickle.load(f)
    f.close()

    print('Total {} pickled feature definitions loaded.'.format(len(features_definition)))
    return features_definition
