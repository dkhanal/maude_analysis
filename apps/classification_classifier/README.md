maude_classification

This application performs the classification of each record in the input files into the following binary classes:

- Positive
- Negative

The input files are supplied through configuration (see config.json). The models to be used for classification are also supplied through configuration.

The following 10 models are supported:

nltk.naive_bayes_bow_no_duplicates: Naive Bayes classification using the bag-of-words approach. The featureset is made of unigrams in the input record. The trained model includes only one of multiple semantically identical records (if any) in the training set.

nltk.naive_bayes_bow_with_duplicates: Naive Bayes classification using the bag-of-words approach. The featureset is made of unigrams in the input record. The trained model may contain multiple semantically identical records in the training set.

nltk.naive_bayes_bigrams_no_duplicates: Naive Bayes classification using the bag-of-words approach. The featureset is made of bigrams in the input record. The trained model includes only one of multiple semantically identical records (if any) in the training set.

nltk.naive_bayes_bigrams_with_duplicates: Naive Bayes classification using the bag-of-words approach. The featureset is made of bigrams in the input record. The trained model may contain multiple semantically identical records in the training set.

nltk.naive_bayes_trigrams_no_duplicates:  Naive Bayes classification using the bag-of-words approach. The featureset is made of trigrams in the input record. The trained model includes only one of multiple semantically identical records (if any) in the training set.

nltk.naive_bayes_trigrams_with_duplicates: Naive Bayes classification using the bag-of-words approach. The featureset is made of trigrams in the input record. The trained model may contain multiple semantically identical records in the training set.

sklearn.sgd_with_duplicates: Stochastic Gradient Descent classification using the term-frequency times inverse document-frequency (tf-idf) approach. The featureset is made of vectors based on word frequency in the input record. The trained model includes only one of multiple semantically identical records (if any) in the training set.

sklearn.sgd_no_duplicates: Stochastic Gradient Descent classification using the term-frequency times inverse document-frequency (tf-idf) approach. The featureset is made of vectors based on word frequency in the input record. The trained model may contain multiple semantically identical records in the training set.

sklearn.voting_with_duplicates: Voting-based classification (voting models: Logistic Regression and Multinomial Naive Bayes) using the term-frequency times inverse document-frequency (tf-idf) approach. The featureset is made of vectors based on word frequency in the input record. The trained model includes only one of multiple semantically identical records (if any) in the training set.

sklearn.voting_no_duplicates: Voting-based classification (voting models: Logistic Regression and Multinomial Naive Bayes) using the term-frequency times inverse document-frequency (tf-idf) approach. The featureset is made of vectors based on word frequency in the input record. The trained model may contain multiple semantically identical records in the training set.


To Run:

```
python main.py
```

For cloud-integration, make sure to add a file called .setenv.py and include these lines:

```
import os

os.environ['azure_account_name'] = '<azure account name>'
os.environ['azure_account_key'] = '<azure account key>'

```