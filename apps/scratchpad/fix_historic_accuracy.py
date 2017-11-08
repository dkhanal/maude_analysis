# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

# For the first ~1000 of the verified sample generator run, models were penalized on accuracy, if human veto was 'unknown' (indeterminate)
# This would  unfairly affect the models' historic feedback accuracy. So this program was written to fix the existing accuracy records.
# Essentially, if human made the decision to classify a record as 'unknown', then each model making the recommendation is 
# considered to have been correct, no matter the recommended classification.
# 
# The fix was also made in the sample generator code to not penalize the models on 'unknown' classification going forward. 

import os
import json


def get_already_read_records(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_already_read_records(file_path, json_data):
    with open(file_path, 'w') as f:
        f.write(json.dumps(json_data, indent=4))


def fix_accuracy():
    data_dir = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_verified_sample_generator\out'

    final_decision_file_path = 'already_processed_record_numbers.json'

    accuracy_files = [
        'nltk.naive_bayes_bow_no_duplicates_accuracy.json',
        'nltk.naive_bayes_bow_with_duplicates_accuracy.json',
        'nltk.naive_bayes_bigrams_no_duplicates_accuracy.json',
        'nltk.naive_bayes_bigrams_with_duplicates_accuracy.json',
        'nltk.naive_bayes_trigrams_no_duplicates_accuracy.json',
        'nltk.naive_bayes_trigrams_with_duplicates_accuracy.json',
        'sklearn.sgd_no_duplicates_accuracy.json',
        'sklearn.sgd_with_duplicates_accuracy.json',
        'sklearn.voting_no_duplicates_accuracy.json',
        'sklearn.voting_with_duplicates_accuracy.json',
        'overall.decision_support_accuracy.json',
        ]

    processed_record_ids = []
    with open(os.path.join(data_dir, final_decision_file_path)) as f:
        decision_data = json.load(f)

    for input_file_name in decision_data:
        records_processed = decision_data[input_file_name]

        for line_number in records_processed:
            decisions = records_processed[line_number]

            for decision in decisions:
                for recordid in decision:
                    processed_record_ids.append(recordid)

    print('Total {} records processed from {}'.format(len(processed_record_ids), final_decision_file_path))


    for accuracy_filename in accuracy_files:
        accuracy_file_path = os.path.join(data_dir, accuracy_filename)

        with open(os.path.join(data_dir, accuracy_file_path)) as f:
            accuracy_data = json.load(f)
            for item in accuracy_data:
                recordid = item['recordid']

                if not recordid in processed_record_ids:
                    print('RECORD ID {} from file {} is NOT in the list of processed records. It was likely classified Unknown'.format(recordid, accuracy_filename))
                    item['correct'] = True # If human cannot determine the classification, machine's classification is correct. 
                else:
                    print('RECORD ID {}  from file {} is in the list of processed record ids'.format(recordid, accuracy_filename))

            save_already_read_records(accuracy_file_path+'.fixed', accuracy_data)

fix_accuracy()
