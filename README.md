# maude_experiments


This repository contains a set of programs that implements natural-language-processing (NLP)-based machine learning techniques to classify the Manufacturer and User Facility Device Experience (MAUDE) dataset published by the US Food and Drugs Administration (FDA).

Each MAUDE record contains an open-ended texual narrative entered by the submitter of the adverse event. Using the NLP techniques against this narrative, we try to classifiy the record as either:

* Software-related event (aka 'positive')
* Non software-related event (aka 'negative')

The input data set is available on https://maude.blob.core.windows.net/narratives. In order to run the programs in this repository, this data must first be downloaded (one-time). You could simply run the following script to download the data files:

```
$ python download_data.py 
```


This repository is divided mainly into three apps:

1. Labeling Application (maude_labeling)

The MAUDE dataset published by the FDA is not labeled. The Labeling application goes through each file in the MAUDE dataset and determines if a particular record is 'positive' or 'negative' with a reasonably high degree of certainty. To achieve this level of certainty, explict and strong string matches are performed. The output of this application are a set of these files:

`<input_filename>.pos.txt` => Positive records
`<input_filename>.neg.txt` => Negative records
`<input_filename>.maybe.neg.txt` => Potentially negative records, but were rejected due to a potential positive signal.
`<input_filename>.maybe.pos.txt` => Potentially positive records, but were rejected due to a potential negative signal.
`<input_filename>.process.txt` => A processing log file with a specific reason for why a particular record was deemed positive or negative.

The output files are persisted in the output folder, as well as on the Cloud.

To run this application, simply execute the main script:
```
$ python main.py
```

This application also conains script that goes through the process log file and instantly provide answer on why a record was selected:

```
$ python why.py <record id>
```


2. Modeling Application (maude_modeling)

The modeling application takes a set of labeled files as input and creates machine learning models. Labeled files are automatically downloaded from the Cloud. Trained models are then persisted in the output folder, and also uploaded to the Cloud. To run the application, simply run the main script:

```
$ python main.py
```

3. Classification Application (maude_classification)

The classification application takes a set of files as input and trained models and performs classification using supported NLP algoritms in the models. Trained models (Output of the Modeling Applications) are automatically downloaded form the Cloud, and the result of the classification also posted to the Cloud. To run the classification application, simply run the main script:

```
$ python main.py
```

See configuration file for the input, ouput and processing parameters.
