import datetime
import os
import nltk
from nltk.corpus import stopwords
import random
from nltk import word_tokenize
import data_access
import util
import config
          
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

    all_words_fd = nltk.FreqDist(list_of_words)
    return list(all_words_fd.keys())[:max]

def tag(dataset, tag):
    return [(w, tag) for w in dataset]


def run_experiment(run_mode = 'sim'):
    print('Starting experiment run at {}'.format(datetime.datetime.now()))

    if run_mode == 'real':
        data_files = config.data_files_real_mode
    else:
        data_files = config.data_files_sim_mode

    print('Running in {} mode...'.format(run_mode))

    print('Known positive signals used for this experiment written to: {}'.format(config.known_positive_records_limit))
    print('Potntial positive signals used for this experiment written to: {}'.format(config.known_positive_records_limit))


    print('Obtaining up to {} known positive records...'.format(config.known_positive_records_limit))
    known_positive_records = data_access.get_known_positives(data_files, config.known_positive_records_limit)
    util.dump_list_to_file(known_positive_records, config.output_files['known_positive_records'])

    print('Obtaining up to {} known negative records...'.format(config.known_negative_records_limit))
    known_negative_records = data_access.get_known_negatives(data_files, config.known_negative_records_limit)
    util.dump_list_to_file(known_negative_records, config.output_files['known_negative_records'])

    print('Tokenizing positive words...')
    words_in_known_positive_records =  [word for line in known_positive_records for word in word_tokenize(line)]

    print('Tokenizing negative words...')
    words_in_known_negative_records =  [word for line in known_negative_records for word in word_tokenize(line)]

    stop_words = stopwords.words('english')

    print('Removing stopwords from positive words...')
    words_without_stopwords_in_known_positive_records = [word for word in words_in_known_positive_records if len(word) > 1 and word.lower() not in stop_words]
    util.dump_list_to_file(words_without_stopwords_in_known_positive_records, config.output_files['known_positive_words'])

    print('Removing stopwords from negative words...')
    words_without_stopwords_in_known_negative_records = [word for word in words_in_known_negative_records if len(word) > 1 and word.lower() not in stop_words]
    util.dump_list_to_file(words_without_stopwords_in_known_negative_records, config.output_files['known_negative_words'])

    print('Obtaining up to {} most common words from positive records...'.format(config.most_common_words_limit))
    most_common_positive_words = extract_most_common_words(words_without_stopwords_in_known_positive_records, config.most_common_words_limit)
    util.dump_list_to_file(most_common_positive_words, config.output_files['most_common_positive_words'])

    print('Tagging known data sets...')
    known_positives_tagged = tag(words_without_stopwords_in_known_positive_records, 'SW_CAUSED')
    known_negatives_tagged = tag(words_without_stopwords_in_known_negative_records, 'NOT_SW_CAUSED')

    print('Building training set...')
    known_tagged = known_positives_tagged + known_negatives_tagged

    print('Building feature set..')
    featureset = [(build_features(list_of_words, most_common_positive_words), tag) for (list_of_words, tag) in known_tagged]
    random.shuffle(featureset)
  
    half_mark = len(featureset) // 2
    print('Half of featureset list is: {}'.format(half_mark))

    training_set = featureset[:half_mark]
    testing_set = featureset[half_mark:]

    print('Training Naive Bayes classifier...')
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print('Training Naive Bayes classifier accuracy is: {}'.format(nltk.classify.accuracy(classifier, testing_set)))
    classifier.show_most_informative_features(100)

    print('Experiment completed at {}'.format(datetime.datetime.now()))