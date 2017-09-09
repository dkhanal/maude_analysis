import numpy
import sys
import time

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer

data_train = fetch_20newsgroups(subset='train', categories=None,
                                shuffle=True, random_state=42)

data_test = fetch_20newsgroups(subset='test', categories=None,
                               shuffle=True, random_state=42)


print(type(data_train))
print(data_train.keys())
print(data_train['filenames'])
print(len(data_train['target_names']))
print(data_train['target_names'])
print(len(data_train['data']))
print(data_train['data'][0])
