# By Deepak Khanal
# dkhanal@gmail.com

import datetime
import os
import nltk
import pickle
import random
import data_access
import util
import config
from nltk.corpus import stopwords
from nltk import word_tokenize
from foi_text import FoiTextRow
         
def build_features(list_of_words, known_feature_words):
    unique_words = set(list_of_words)
    features = {}
    for w in known_feature_words:
        features[w] = (w in unique_words)
    return features

def extract_most_common_words(list_of_words, max):
    print('Extracting most common up to {} words...'.format(max))
    print('There are total {} words in the list. Computing frequency distribution...'.format(len(list_of_words)))
    if list_of_words is None or  len(list_of_words) == 0:
        return []
    
    # Eliminate punctuations, 'words' with less than 3 letters, and noise words
    list_of_words = [w for w in list_of_words if len(w) > 2 and not w in config.noise_words]

    all_words_fd = nltk.FreqDist(list_of_words)
    return [w for (w, f) in all_words_fd.most_common(max)]

def tag(dataset, tag):
    return [(w, tag) for w in dataset]


def create_models():
    start_time = datetime.datetime.now()
    print('create_models() starting at {}'.format(start_time))

    data_files = config.data_files_for_featureset

    print('Known positive signals used for this experiment written to: {}'.format(config.output_files['known_positive_signals']))
    util.dump_list_to_file(config.known_positive_signals, config.output_files['known_positive_signals'])

    print('Potential positive signals used for this experiment written to: {}'.format(config.output_files['potential_positive_signals']))
    util.dump_list_to_file(config.potential_positive_signals, config.output_files['potential_positive_signals'])

    print('Obtaining up to {} known positive records...'.format(config.known_positive_records_limit))
    known_positive_records = data_access.get_known_positives(data_files, config.known_positive_records_limit)
    util.dump_list_to_file(known_positive_records, config.output_files['known_positive_records'])

    print('Obtaining up to {} known negative records...'.format(config.known_negative_records_limit))
    known_negative_records = data_access.get_known_negatives(data_files, config.known_negative_records_limit)
    util.dump_list_to_file(known_negative_records, config.output_files['known_negative_records'])

    print('Word-tokenizing positive records...')
    words_in_known_positive_records =  [word for line in known_positive_records for word in word_tokenize(line)]

    print('Word-tokenizing negative records...')
    words_in_known_negative_records =  [word for line in known_negative_records for word in word_tokenize(line)]

    stop_words = stopwords.words('english')

    print('Removing stopwords from positive words...')
    words_without_stopwords_in_known_positive_records = [word for word in words_in_known_positive_records if len(word) > 1 and word.lower() not in stop_words]
    util.dump_list_to_file(words_without_stopwords_in_known_positive_records, config.output_files['known_positive_words'])

    print('Removing stopwords from negative words...')
    words_without_stopwords_in_known_negative_records = [word for word in words_in_known_negative_records if len(word) > 1 and word.lower() not in stop_words]
    util.dump_list_to_file(words_without_stopwords_in_known_negative_records, config.output_files['known_negative_words'])

    print('Stemming words...')
    stemmer = nltk.stem.PorterStemmer()
    stemmed_words_without_stopwords_in_known_positive_records = [stemmer.stem(w) for w in words_without_stopwords_in_known_positive_records]
    stemmed_words_without_stopwords_in_known_negative_records = [stemmer.stem(w) for w in words_without_stopwords_in_known_negative_records]

    print('Obtaining up to {} most common words from positive records...'.format(config.most_common_words_limit))
    feature_words = extract_most_common_words(stemmed_words_without_stopwords_in_known_positive_records, config.most_common_words_limit)
    util.dump_list_to_file(feature_words, config.output_files['feature_words'])

    print('Tagging known data sets...')
    known_positives_tagged = tag(stemmed_words_without_stopwords_in_known_positive_records, config.tag_positive)
    known_negatives_tagged = tag(stemmed_words_without_stopwords_in_known_negative_records, config.tag_negative)

    print('Building training set...')
    known_tagged = known_positives_tagged + known_negatives_tagged

    print('Building feature set..')
    featureset = [(build_features(list_of_words, feature_words), tag) for (list_of_words, tag) in known_tagged]
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

    return (classifiers, feature_words)

def classify(classifiers, feature_words, skip_first_line=True, max = None):
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
            positive_record_ids = classify_file(full_file_path, classifier_name, classifier_obj, feature_words, skip_first_line)
            util.dump_list_to_file(positive_record_ids, config.output_files['predicted_positive_records'])

    end_time = datetime.datetime.now()
    print('classify() completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


def classify_file(file_path, classifier_name, classifier, feature_words, skip_first_line=True):
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
                sys.stdout.flush()

            if len(row.foi_text.strip()) < 50: # Insufficient size of narrative text
                continue

            line_to_classify = row.foi_text.upper()
            words_to_classify = word_tokenize(line_to_classify)
            
            stemmer = nltk.stem.PorterStemmer()

            stemed_words_to_classify = [stemmer.stem(w) for w in words_to_classify]
            line_features = build_features(stemed_words_to_classify, feature_words)

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

def pickle_feature_words(list_of_words):
    pickle_file = config.output_files['feature_words_pickle']
    if not os.path.isabs(pickle_file):
        pickle_dir = config.pickles_save_dir
        if not os.path.isabs(pickle_dir):
            pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)
        pickle_file = os.path.join(pickle_dir, pickle_file)


    print('Pickling feature words as: {}...'.format(os.path.basename(pickle_file)))
    f = open(pickle_file, 'wb')
    pickle.dump(list_of_words, f)
    f.close()

def load_pickled_feature_words():
    pickle_file = config.output_files['feature_words_pickle']
    if not os.path.isabs(pickle_file):
        pickle_dir = config.pickles_save_dir
        if not os.path.isabs(pickle_dir):
            pickle_dir = os.path.join(os.path.dirname(__file__), pickle_dir)
        pickle_file = os.path.join(pickle_dir, pickle_file)


    print('Loading pickled feature words from: {}...'.format(os.path.basename(pickle_file)))
    if not os.path.isfile(pickle_file):
        print ('Pickle file does not exist.')
        return []

    f = open(pickle_file, 'rb')
    feature_words = pickle.load(f)
    f.close()

    print('Total {} pickled feature word(s) loaded.'.format(len(feature_words)))
    return feature_words
