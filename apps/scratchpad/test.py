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
from sklearn.ensemble import VotingClassifier

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def get_records(filenames):
    for filename in filenames:
        with open(filename) as f:
            for line in f:
                yield line


pos_file_path = os.path.abspath(os.path.join('..', 'maude_labeling', 'out', 'potential_positive_records.txt'))
neg_file_path = os.path.abspath(os.path.join('..', 'maude_labeling', 'out', 'potential_negative_records.txt'))

print('Positive labeled file is: {}'.format(pos_file_path))
print('Negative labeled file is: {}'.format(neg_file_path))

positive_file_total_records = get_total_lines_count(pos_file_path)
negative_file_total_records = get_total_lines_count(neg_file_path)

labels = (['pos'] * positive_file_total_records) + (['neg'] * negative_file_total_records)

print('Length of lables is {}'.format(len(labels)))

vectorizer = CountVectorizer(input='content')

x_train = vectorizer.fit_transform(get_records([pos_file_path, neg_file_path])) # Builds a sparse matrix

# print(vectorizer.get_feature_names())
print(x_train.shape)

tf_transformer = TfidfTransformer(use_idf=False).fit(x_train)
x_train_tf = tf_transformer.transform(x_train)
print(x_train_tf.shape)


# print (labels)


clf = SGDClassifier(loss='log').fit(x_train_tf, labels)

clf1 = LogisticRegression(random_state=1)
clf2 = MultinomialNB()
eclf1 = VotingClassifier(estimators=[('lr', clf1), ('mnb', clf2)], voting='soft')
eclf1 = eclf1.fit(x_train_tf, labels)


print (clf)

docs_new = ['There was a memory overwrite error.']
x_new_counts = vectorizer.transform(docs_new)
x_new_tfidf = tf_transformer.transform(x_new_counts)

predicted = clf.predict(x_new_tfidf)
predicted_prob = clf.predict_proba(x_new_tfidf)

index_of_pos = numpy.where(clf.classes_ == 'pos')
print (predicted)
print(predicted_prob)
print ('Probability of pos: ')
print(predicted_prob[0][index_of_pos][0])


print(eclf1.predict(x_new_tfidf))
print(eclf1.predict_proba(x_new_tfidf))