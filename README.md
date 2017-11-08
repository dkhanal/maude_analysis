# maude_experiments


This repository contains a set of programs that implements natural-language-processing and machine learning techniques to classify the Manufacturer and User Facility Device Experience (MAUDE) dataset published by the US Food and Drugs Administration (FDA).

Each MAUDE record contains an open-ended texual narrative entered by the submitter of the adverse event. Using the NLP techniques against this narrative, we try to classifiy the record as either:

* Computing technology-related event (aka 'positive')
* Not computing technology-related event (aka 'negative')

The input data set is available on https://maude.blob.core.windows.net/narratives. In order to run the programs in this repository, this data must first be downloaded (one-time). You could simply run the following script to download the data files:

```
$ python download_data.py 
```
======

This repository is divided mainly into five applications (and a shared library):

##1. [Labeling Candidate Extractor](apps/labeling_candidate_extractor)

This application goes through a set of input files and extracts candidate positive and negative records for labeling. 

##2. [Verified Sample Generator](apps/labeling_verified_sample_generator)

This application allows the User to perform manual labeling of records. The objective is to generate a carefully curated set of positive and negative records, that could be used as seeds to generate more training records to train the computer models. The output of the first application serves as the input to this application.

##3. [Auto Labeler](apps/labeling_auto_labeler)

This application takes as input the output of the first two applications and performs an iterative auto-labeling with integrated quality control (QC). Labeling is based on classification using a high-accuracy model. The model is re-trained after each QC.

##4. [Trained Model Generator](apps/modeling_trained_model_generator)

This application generates a set of trained computer models based on the labeled records (output from Auto Labeler application). 

##5. [Classifier](apps/classification_classifier)

This application performs the classification of each record in the input file set to either positive or negative. A set of computer models are used to make this classification.

Each of these five applications shares a library of common functions. The library is in the shared directory.




To run any of these programs, simply run the main script inside the application's directory:

```
$ python main.py
```

Each application has a configuration file that you can use to adjust its runtime behavior.


