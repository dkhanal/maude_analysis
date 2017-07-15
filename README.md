# maude_sw_causes


This repository contains a program that implements natural-language-processing (NLP)-based machine learning techniques to classify the Manufacturer and User Facility Device Experience (MAUDE) dataset published by the US Food and Drugs Administration.

More specifically, each record of narrative text that describes a medical device adverse event in the MAUDE dataset is classified in terms of its causality as either:

* Software-related event
* Non software-related event

At a high-level, this program supports two methods:

1. Fixed Features:
A set of NLP features can be defined in the configuration file. Each feature has a name, words to match and minimumum required matches. All three attributes are pre-defined by the researcher and specified in the config file. Then model is trained using this feature definition. The trained model, then is used to classify the corpus.

2. Dynamic Features
Features are dynamically extracted from 'known' positive records. Essentially, most common n words (where n is configurable) that occur in the known positive records are defined as the features. The model is trained using this dynamic feature definition. The trained model, then is used to classify the corpus.

Regardless of the methods used, the following is the high level process:

Model Creation

1. Configuration is loaded (note, the program supports a variety of configuration options)
2. 'Known' positive records are loaded. This is done by scanning a subset of the corpus, with explicit, traditional form of string comparison that yields a strong match. Configuration file contains parameters used to perform this match. The number of positive records to extract from the corpus is also configurable.
3. 'Known' negative records are loaded. Similar to the previous step, this is also done by scanning a subset of the corpus, with explicit, traditional form of string comparison that yields a strong match. Configuration file contains parameters used to perform this match. Essentially, a negative record is selected by determining that none of the potention signals that could qualify the record to be positive is present.
4. Records (known-positive and known-negative) are word-tokenized.
5. Stop words are removed from both word-tokenized known-positive and known-negative records.
6. Words are stemmed for both known positive and known-negative records.
7. Known positive and known-negative records are appropriately tagged.
8. Feature definition is built (using either Fixed or Dyanamic option).
9. Featureset is built using the Feature definition and the known records (positive and negative)
10. Model is trained using a subset of the featureset. Currently, Naive Bayes Classifier is used as the model. However, the design allows for additional models to be supported.

Trained models can be 'pickled' for future use. Configuration options are available for pickling and using pickled models.

Text Classification

1. Model is loaded (either by the virtue of Model Creation or loading from the pickled copy)
2. Corpus is loaded (one record at a time)
3. Corpus record is word tokenized.
4. Stopwords are removed from the corpus record.
5. Corpus record is stemmed.
6. Features are built for the corpus record.
7. Features are provided to the model for classification.
8. Final classification is based on the model's categorical response and the probability reported on the response. Only classification meeting a probability threshold (configurable) are finally classified as positive.


