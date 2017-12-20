# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import json
import random
import logging
import datetime
import re
import math
import hashlib
import shutil

import sharedlib
import config


import __remote_server_helper
import __modeling_helper
import __classification_helper

global positive_class_str
global negative_class_str
positive_class_str = 'pos'
negative_class_str = 'neg'


def label_records(mode):
    input_files = config.input_data_files
    logging.info('Auto-labeling known positive and negative records from {} file(s)...'.format(len(input_files)))
 
    autolabeled_positive_records_file = sharedlib.abspath(config.output_files['autolabeled_positive_records_file'])
    autolabeled_negative_records_file = sharedlib.abspath(config.output_files['autolabeled_negative_records_file'])

    input_file_total_lines_count_file = sharedlib.abspath(config.output_files['input_file_total_lines_count_file'])
    already_processed_record_numbers_file = sharedlib.abspath(config.output_files['already_processed_record_numbers_file'])
    
    existing_work_in_progress = __remote_server_helper.all_work_in_progress_files_present_on_remote_server(config.remote_server, config.remote_server_files)
    if existing_work_in_progress:
        __remote_server_helper.download_remote_server_files(config.remote_server, config.remote_server_files, config.output_files)
    else:
        logging.info('This appears the first auto-labeling session. Labeled seeds files now will be downloaded from the remote server...')
        __remote_server_helper.download_labeled_seed_files(config.remote_server, config.remote_server_files, config.output_files)


    models = __remote_server_helper.download_models_from_remote_server(config.remote_server, config.models, config.models_output_dir)

    autolabel(mode, input_files, autolabeled_positive_records_file, autolabeled_negative_records_file, already_processed_record_numbers_file, input_file_total_lines_count_file, models)
    
    sharedlib.remove_duplicate_records([autolabeled_negative_records_file, autolabeled_positive_records_file])

    if config.upload_output_to_remote_server == True:
        logging.info('Upload output{}? [y/n] '.format( '' if existing_work_in_progress else ' (POTENTIALLY OVERWRITE CLOUD)'))
        upload_confirmation = sharedlib.get_char_input()
        if not isinstance(upload_confirmation, str):
            upload_confirmation = bytes.decode(upload_confirmation)
        if upload_confirmation == 'y':
            files_to_upload = [autolabeled_positive_records_file, autolabeled_negative_records_file, already_processed_record_numbers_file]
            sharedlib.upload_files_to_remote_server(files_to_upload, config.remote_server['labeling_auto_labeled_dir'])


def get_total_available_records(file_path):
    logging.info('Reading total available records info...')
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        return json.load(f)


def save_total_available_records(file_path, json_data):
    logging.info('Saving total available records info...')
    with open(file_path, 'w') as f:
        f.write(json.dumps(json_data, indent=4))


def get_already_read_records(file_path):
    logging.info('Reading the already processed record numbers...')
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        return json.load(f)

def save_already_read_records(file_path, json_data):
    logging.info('Saving already processed record numbers...')
    with open(file_path, 'w') as f:
        f.write(json.dumps(json_data, indent=4))

def get_total_lines_count(file_path):
    return sharedlib.get_total_lines_count(file_path)

def get_unique_random_record_number(total_autolabled_positive_records, already_read_record_numbers):
   all_possible = set(range(1, total_autolabled_positive_records+1))
   already_read = set(already_read_record_numbers.keys())
   eligible_record_numbers = all_possible.difference(already_read)
   
   choice = random.choice(list(eligible_record_numbers))
   logging.info('All possible in this file: {}, already read: {} eligible: {}, randomly selected: {}'.format(len(all_possible), len(already_read), len(eligible_record_numbers), choice))
   return choice

def get_line(file_to_read, record_number_to_read):
    with open(file_to_read, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = 0
        for line in f:
            line_count += 1
            if line_count == record_number_to_read:
                return line
    return 'NO RECORD FOUND AT LINE NUMBER {} IN {}'.format(record_number_to_read, file_to_read)

def bulk_open_files(files_paths_to_open, mode):
    file_handles = []

    if files_paths_to_open is None:
        return file_handles

    for file_path in files_paths_to_open:
        file_handles.append(open(file_path, mode, encoding='utf-8', errors='ignore'))

    return file_handles

def bulk_close_files(file_handles_to_close):
    if file_handles_to_close is None:
        return

    for fh in file_handles_to_close:
        fh.close()

def remove_semantically_duplicate_records(file_path, dup_check_ignore_pattern_regex, max_number_of_duplicates_to_tolerate):
    record_hash_dict = {}
    subset = []
    read_record_count = 0
    with open(file_path, 'r',  encoding='utf-8', errors='ignore') as fin:
        for line in fin:
            read_record_count += 1
            record_to_hash = None
            if dup_check_ignore_pattern_regex is not None:
                record_to_hash = re.sub(dup_check_ignore_pattern_regex, '', line)
            else:
                record_to_hash = line
                        
            record_hash = hashlib.sha1(record_to_hash.upper().encode(errors='ignore')).hexdigest()
            
            if record_hash in record_hash_dict:
                current_duplicate_count = record_hash_dict[record_hash]
                if current_duplicate_count >= max_number_of_duplicates_to_tolerate:
                    logging.info('Record {} already has {} duplicates, which is maximum tolerated number of duplicates. It will be eliminated.'.format(line[:40], current_duplicate_count))
                    continue
                record_hash_dict[record_hash] = current_duplicate_count + 1
            else:
                record_hash_dict[record_hash] = 1

            subset.append(line)

    written_record_count = 0
    with open(file_path, 'w',  encoding='utf-8', errors='ignore') as fout:
        for line in subset:
            fout.write(line)
            written_record_count += 1

    logging.info('Eliminated {} semantically duplicate records from {}. Read: {}, Written: {}'.format(read_record_count - written_record_count, os.path.basename(file_path), read_record_count, written_record_count))

    return record_hash_dict


def perform_random_qc(population, eligible_population_size, sample_size, expected_class):    
    population_size = len(population)
    if eligible_population_size > population_size:
        eligible_population_size = population_size

    if sample_size > eligible_population_size:
        sample_size = eligible_population_size

    eligible_population_index_range = range(max(0, population_size - eligible_population_size), population_size)
    print('Population size {}, sample size {}'.format(population_size, sample_size))
    sample_indices = random.sample(eligible_population_index_range, min(sample_size, len(eligible_population_index_range)))

    expected_class_char_0 = expected_class[0].lower()
    logging.info('Random QC will be performed on {} {} samples from {} eligible items..'.format(len(sample_indices), expected_class, len(eligible_population_index_range)))

    false_classified_indices = set()
    indeterminate_indices = set()

    user_aborted = False

    record_count = 0
    total_samples = len(sample_indices)
    for index in sample_indices:
        # Each item in the population list has the record in the 0th index, positive probability in index 1.
        record = population[index][0]  
        pos_proba = population[index][1]
        record_count += 1
        logging.info('Record #{} (QC sample #{} of {}). Positive Probability: {:.2f}, Negative: {:.2f}'.format(index, record_count, total_samples, pos_proba, 1-pos_proba))
        logging.info(record)

        logging.info('')
        logging.info('[P]ositive, [N]egative, [U]nknown?, [Q]uit')
        logging.info('')

        decision = None
        while (decision != 'p' and decision != 'n' and decision != 'u' and decision != 'q'):
            decision = sharedlib.get_char_input()
            if not isinstance(decision, str):
                decision = bytes.decode(decision)
            decision = decision.lower()

        logging.info('Selected: {}'.format(decision))
        if decision == expected_class_char_0:
            continue # Classification confirmed

        if decision == 'q':
            logging.info('QC exited by User'.format(index))
            user_aborted = True
            break;

        if decision == 'u':
            logging.info('Item # {} corrected as unknown'.format(index))
            indeterminate_indices.add(index)
        else:
            logging.info('Item # {} corrected as falsely classified'.format(index))
            false_classified_indices.add(index)

    total_qced_records = record_count -1 if user_aborted == True else record_count
    logging.info('Random QC performed on {} {} samples. {} Falsely classified and {} indeterminate'.format(total_qced_records, expected_class, len(false_classified_indices), len(indeterminate_indices)))
    return (false_classified_indices, indeterminate_indices, total_qced_records, user_aborted)

def order_by_pos_probability(model, records, reverse_ordered, class_str):
    logging.info('Ordering {} {} items by positive probability in {} order...'.format(len(records), class_str, 'reverse' if reverse_ordered else 'ascending'))
    classified_records = []

    for record in records:
        (model_name, result) = __classification_helper.classify(record, [model])[0]
         # returns tuple: (name, (predicted_classification, positive_proba))
        classified_records.append((record, result[1]))

    classified_records.sort(key=lambda item: item[1], reverse = reverse_ordered)
    return classified_records


def perform_manual_qc(model, positive_records_file_path, 
                      negative_records_file_path,
                      qc_eligible_population_size,
                      qc_sample_size):

    logging.info('Performing manual QC...')

    if qc_sample_size > qc_eligible_population_size:
        qc_sample_size = qc_eligible_population_size

    positive_records = sharedlib.read_all_records(positive_records_file_path)
    negative_records = sharedlib.read_all_records(negative_records_file_path)

    # Put potential outliers/falsely classified at the bottom of the list
    positive_records_sorted = order_by_pos_probability(model, positive_records, True, positive_class_str) # Order by highest pos probability to lowest
    negative_records_sorted = order_by_pos_probability(model, negative_records, False, negative_class_str)  # Order by lowest pos probability to highest

    (false_positive_indices,  positive_but_indeterminate_indices, total_qced_positive_records, positive_qc_user_aborted) = perform_random_qc(positive_records_sorted, qc_eligible_population_size, qc_sample_size, positive_class_str)
    (false_negative_indices,  negative_but_indeterminate_indices, total_qced_negative_records, negative_qc_user_aborted) = perform_random_qc(negative_records_sorted, qc_eligible_population_size, qc_sample_size, negative_class_str)

    total_misclassified = len(false_positive_indices) + len(false_negative_indices)
    total_indeterminate = len(positive_but_indeterminate_indices) + len(negative_but_indeterminate_indices)
    total_qced = total_qced_positive_records + total_qced_negative_records

    # Join the sets to obtain the superset of removal candidates
    positive_indices_to_remove = false_positive_indices | positive_but_indeterminate_indices
    negative_indices_to_remove = false_negative_indices | negative_but_indeterminate_indices

    # List comprehension
    false_positive_records = [positive_records_sorted[i][0] for i in false_positive_indices]    # Each item in the sorted list has the record in the 0th index, probability in index 1.
    false_negative_records = [negative_records_sorted[i][0] for i in false_negative_indices]   
    
    true_positive_records = [record for i, (record, proba) in enumerate(positive_records_sorted) if not i in positive_indices_to_remove]
    true_negative_records = [record for i, (record, proba) in enumerate(negative_records_sorted) if not i in negative_indices_to_remove]

    new_positive_records = true_positive_records + false_negative_records
    new_negative_records = true_negative_records + false_positive_records

    sharedlib.save_list_to_file(new_positive_records, positive_records_file_path)
    sharedlib.save_list_to_file(new_negative_records, negative_records_file_path)

    qc_score = 0 if total_qced == 0 else ((total_qced - (total_misclassified + total_indeterminate)) / total_qced)
    logging.info('Manual QC of total {} records found {} misclassified ({} false positives + {} false negatives) and {} indeterminate records. Overall QC score: {:.2f}.'.format(total_qced, total_misclassified, len(false_positive_indices), len(false_negative_indices), len(positive_but_indeterminate_indices|negative_but_indeterminate_indices), qc_score))

    return (qc_score, positive_qc_user_aborted or negative_qc_user_aborted)


def autolabel(mode, 
         input_files,
         autolabeled_positive_records_file_path, 
         autolabeled_negative_records_file_path, 
         already_processed_record_numbers_file_path, 
         input_file_total_lines_count_file_path, model):
        
    autolabled_positive_records_file_basename = os.path.basename(autolabeled_positive_records_file_path).lower()
    autolabled_negative_records_file_basename = os.path.basename(autolabeled_negative_records_file_path).lower()

    autolabled_pos_duplicates_table = remove_semantically_duplicate_records(autolabeled_positive_records_file_path, config.duplicate_record_check_ignore_pattern, config.max_semantic_duplicate_records_allowed)
    autolabled_neg_duplicates_table = remove_semantically_duplicate_records(autolabeled_negative_records_file_path, config.duplicate_record_check_ignore_pattern, config.max_semantic_duplicate_records_allowed)

    sharedlib.remove_duplicate_records([autolabeled_positive_records_file_path, autolabeled_negative_records_file_path])
    
    # Perform QC of the master labeled set    
    while True:
        # QC until it passes 100% or user skips
        new_model = __modeling_helper.rebuild_models(autolabeled_positive_records_file_path, autolabeled_negative_records_file_path, already_processed_record_numbers_file_path, input_file_total_lines_count_file_path)[0]
        (qc_score, user_aborted)  = perform_manual_qc(new_model, autolabeled_positive_records_file_path, autolabeled_negative_records_file_path, 50, 20)

        if qc_score != 1 and user_aborted == False:
            logging.info('QC of the sampling of the entire dataset found at least one correction needed (QC Score: {:.2f}). Performing another round of QC...'.format(qc_score))
            continue

        logging.info('QC (Score: {:.2f}) passed or user skipped. Do you want to continue auto-labeling? [Y]es to continue; [N]o to quit, [R] to re-QC...'.format(qc_score))
        decision = None
        while (decision != 'y' and decision != 'n' and decision != 'r'):
            decision = sharedlib.get_char_input()
            if not isinstance(decision, str):
                decision = bytes.decode(decision)
            decision = decision.lower()

        logging.info('Selected: {}'.format(decision))
        if decision == 'n':
            return;
        elif decision == 'r':
            continue
        else:
            break; # QC of master set complete, exit the loop and continue with auto-labeling.

    total_new_records_labeled_this_session = 0
    autolabeled_positive_records_pending_qc_file_path = sharedlib.abspath(os.path.join(config.output_dir, 'positive_records_pending_qc.txt'))
    autolabeled_negative_records_pending_qc_file_path = sharedlib.abspath(os.path.join(config.output_dir, 'negative_records_pending_qc.txt'))

    # Create the model for auto labeling
    while True:
        logging.info('Confirm to continue with auto-labeling. [Y]es, [N]o: ')
        decision = None
        while (decision != 'y' and decision != 'n'):
            decision = sharedlib.get_char_input()
            if not isinstance(decision, str):
                decision = bytes.decode(decision)
            decision = decision.lower()

        logging.info('Selected: {}'.format(decision))
        if decision == 'n':
            break;

        logging.info('[Re]building model to be used in classification...')

        new_model = __modeling_helper.rebuild_models(autolabeled_positive_records_file_path, autolabeled_negative_records_file_path, already_processed_record_numbers_file_path, input_file_total_lines_count_file_path)[0]
        min_required_model_score = config.min_model_score_for_auto_labeling
        model_score = new_model[3]
        if model_score < min_required_model_score:
            logging.info('Model accuracy score is {}, which is less than the minimum required for auto labeling. Quitting...'.format(model_score, min_required_model_score))
            break
        
        
        total_new_records_labeled_using_current_models = 0
        previous_qc_score = .8 # For the very first QC of the session, we assume 20% failure. This then gets updated with every QC performed.

        input_file_basename_to_full_path_map = {}

        for input_file in input_files:
            input_file_basename_to_full_path_map[os.path.basename(input_file).lower()] = sharedlib.abspath(input_file)

        already_read_records = get_already_read_records(already_processed_record_numbers_file_path)
        if already_read_records is None or len(already_read_records) == 0:
            logging.info('Already read records data not found. Creating new...')
            already_read_records = {}

        for input_file in input_files:
            input_file_basename = os.path.basename(input_file).lower()
            if input_file_basename not in already_read_records:
                already_read_records[os.path.basename(input_file).lower()] = {}

        total_available_records = get_total_available_records(input_file_total_lines_count_file_path)
        if total_available_records is None or len(total_available_records) == 0:
            logging.info('Input file total available records data not found. Creating new...')
            total_available_records = {}

        for input_file in input_files:
            input_file_basename = os.path.basename(input_file).lower()
            if input_file_basename not in total_available_records:
                logging.info('Creating new...')
                total_available_records[os.path.basename(input_file).lower()] = get_total_lines_count(input_file_basename_to_full_path_map[input_file_basename])

        save_already_read_records(already_processed_record_numbers_file_path, already_read_records)
        save_total_available_records(input_file_total_lines_count_file_path, total_available_records)

        total_autolabeled_positive_records = get_total_lines_count(autolabeled_positive_records_file_path) if os.path.exists(autolabeled_positive_records_file_path) else 0
        total_autolabeled_negative_records = get_total_lines_count(autolabeled_negative_records_file_path) if os.path.exists(autolabeled_negative_records_file_path) else 0

        autolabeled_positive_records_pending_qc_file = open(autolabeled_positive_records_pending_qc_file_path, 'w', encoding='utf-8', errors='ignore')
        autolabeled_negative_records_pending_qc_file = open(autolabeled_negative_records_pending_qc_file_path, 'w', encoding='utf-8', errors='ignore')

        total_autolabeled_positive_records_pending_qc = 0
        total_autolabeled_negative_records_pending_qc = 0

        input_file_basenames = [key for key in total_available_records for input_file in input_files if key in input_file.lower()]
        while total_new_records_labeled_using_current_models <= config.models_auto_regen_records_threshold:
            logging.info('-------------------------------------------------------------------')
            file_to_read_basename = None if mode is None else next([file for file in input_file_basenames if file == mode.lower()], None)
            if file_to_read_basename == None:
                file_to_read_basename = random.choice(input_file_basenames)

            file_to_read = None
            aleady_read_record_numbers = already_read_records[file_to_read_basename]
            record_number_to_read = get_unique_random_record_number(total_available_records[file_to_read_basename],
                                                                    aleady_read_record_numbers)
            file_to_read = input_file_basename_to_full_path_map[file_to_read_basename]

            minibatch_labeled_records_count = 0
            minibatch_attempted_records_count =  0

            file_to_read_handle = open(file_to_read, 'r', encoding='utf-8', errors='ignore');
            line_number = 0

            # Advance to the record being read. A 'mini batch' will begin at that location until <minibatch_size> samples are found. 
            logging.info('Locating the record {} in this file...'.format(record_number_to_read))
            while line_number < record_number_to_read:
                next(file_to_read_handle)
                line_number += 1

            configured_minibatch_size = config.minibatch_size
        
            logging.info('Entering minibatch loop for file {}, starting Record# {}. Looking for {} labeled records in this file...'.format(file_to_read_basename, record_number_to_read, configured_minibatch_size))
            while minibatch_labeled_records_count < configured_minibatch_size:
                if minibatch_attempted_records_count != 0:
                    # This means this pass is not the first in the minibatch loop. Advance the record number.
                    record_number_to_read += 1

                if record_number_to_read >= total_available_records[file_to_read_basename]: 
                    # End of the file reached. Exit the minibatch loop to determine the next file and/or entry point
                    break;
            
                if total_new_records_labeled_using_current_models > config.models_auto_regen_records_threshold:
                    # Model re-generation is due
                    break;
                
                logging.info('So far pending QC => POS: {}, NEG: {}. Model accuracy {:.2f}. File: {} Record#: {}. Auto-labeled since last model generation: {}. Still looking for {} labeled in this minibatch.'.format(total_autolabeled_positive_records_pending_qc, total_autolabeled_negative_records_pending_qc, new_model[3], file_to_read_basename, record_number_to_read, total_new_records_labeled_using_current_models, (config.minibatch_size - minibatch_labeled_records_count)))
                line = file_to_read_handle.readline()
                minibatch_attempted_records_count +=1 

                record_hash = hashlib.sha1(re.sub(config.duplicate_record_check_ignore_pattern, '', line).upper().encode(errors='ignore')).hexdigest()

                line_id = line[:40]
                (model_name, result) = __classification_helper.classify(line, [new_model])[0] # returns tuple: (name, (predicted_classification, positive_proba))
        
                pos_prob = result[1]
                neg_prob = 1 - pos_prob

                if pos_prob >= config.min_probability_for_auto_labeling:
                    if (total_autolabeled_positive_records + total_autolabeled_positive_records_pending_qc) > (total_autolabeled_negative_records + total_autolabeled_negative_records_pending_qc):
                        logging.info('This is a positive record, but the search is for a negative record to maintain positive/negative parity. Skipping...')
                        # We maintain positive/negative count parity as we go
                        continue

                    # Do not allow more than n duplicates to prevent bias
                    if record_hash not in autolabled_pos_duplicates_table:
                        autolabled_pos_duplicates_table[record_hash] = 0 # Initialize the hash table entry

                    if autolabled_pos_duplicates_table[record_hash] >= config.max_semantic_duplicate_records_allowed:
                        logging.info('This is a technically unique but semantically duplicate record. There are already {} copies in the positive set. Skipping...'.format(autolabled_pos_duplicates_table[record_hash]))
                        continue

                    autolabled_pos_duplicates_table[record_hash] += 1


                    logging.info(line)
                    logging.info('Auto-Selected: Positive')
                    autolabeled_positive_records_pending_qc_file.write(line)
                    total_autolabeled_positive_records_pending_qc += 1
                    minibatch_labeled_records_count += 1
                    total_new_records_labeled_using_current_models += 1
                    total_new_records_labeled_this_session += 1
                    if not record_number_to_read in already_read_records:
                        aleady_read_record_numbers[record_number_to_read] = []
                    aleady_read_record_numbers[record_number_to_read].append({line_id: positive_class_str})

                elif neg_prob >= config.min_probability_for_auto_labeling:
                    if (total_autolabeled_negative_records + total_autolabeled_negative_records_pending_qc) > (total_autolabeled_positive_records + total_autolabeled_positive_records_pending_qc) :
                        logging.info('This is a negative record, but the search is for a positive record to maintain positive/negative parity. Skipping...')
                        # We maintain positive/negative count parity as we go
                        continue

                    # Do not allow more than n duplicates to prevent bias
                    if record_hash not in autolabled_neg_duplicates_table:
                        autolabled_neg_duplicates_table[record_hash] = 0 # Initialize the hash table entry

                    if autolabled_neg_duplicates_table[record_hash] >= config.max_semantic_duplicate_records_allowed:
                        logging.info('This is a technically unique but semantically duplicate record. There are already {} copies in the negative set. Skipping...'.format(autolabled_neg_duplicates_table[record_hash]))
                        continue

                    autolabled_neg_duplicates_table[record_hash] += 1


                    logging.info(line)
                    logging.info('Auto-selected: Negative')
                    autolabeled_negative_records_pending_qc_file.write(line)
                    minibatch_labeled_records_count += 1
                    total_autolabeled_negative_records_pending_qc += 1
                    total_new_records_labeled_using_current_models += 1
                    total_new_records_labeled_this_session += 1
                    if not record_number_to_read in already_read_records:
                        aleady_read_record_numbers[record_number_to_read] = []
                    aleady_read_record_numbers[record_number_to_read].append({line_id: negative_class_str})

                else:
                    logging.info('This record (POS: {:.2f}, NEG: {:.2f}) is not strong enough (min required: {:.2f}) to be in the labeled set. Skipping...'.format(pos_prob, neg_prob, config.min_probability_for_auto_labeling))
                    continue;

        
                save_already_read_records(already_processed_record_numbers_file_path, already_read_records)

            file_to_read_handle.close()

        autolabeled_positive_records_pending_qc_file.close()
        autolabeled_negative_records_pending_qc_file.close()
        logging.info('{} records auto-labeled since the last model. These new records must be QCed...'.format(total_new_records_labeled_using_current_models))
        while True:
            total_autolabeled_positive_records_pending_qc = sharedlib.get_total_lines_count(autolabeled_positive_records_pending_qc_file_path)
            total_autolabeled_negative_records_pending_qc = sharedlib.get_total_lines_count(autolabeled_negative_records_pending_qc_file_path)
            total_pending_qc_records_count = total_autolabeled_positive_records_pending_qc + total_autolabeled_negative_records_pending_qc
            sample_size =   math.ceil(total_pending_qc_records_count * ((1-previous_qc_score) * config.inaccuracy_to_qc_sample_size_multiplier))
            if sample_size < 1 or sample_size > total_pending_qc_records_count:
                sample_size = total_pending_qc_records_count

            (qc_score, user_aborted) = perform_manual_qc(new_model, autolabeled_positive_records_pending_qc_file_path, autolabeled_negative_records_pending_qc_file_path, total_new_records_labeled_using_current_models, sample_size)

            previous_qc_score = qc_score
            if qc_score != 1 and user_aborted == False:
                logging.info('QC found at least one correction needed (QC Score: {:.2f}). Additional QC will be needed...'.format(qc_score))
                continue

            logging.info('Model re-built and QC (Score: {:.2f}) passed or user skipped. Do you want to merge pending QC records to the master set? [Y]es to continue; [N]o to quit; [R] to re-run QC...'.format(qc_score))
            decision = None
            while (decision != 'y' and decision != 'n' and decision != 'r'):
                decision = sharedlib.get_char_input()
                if not isinstance(decision, str):
                    decision = bytes.decode(decision)
                decision = decision.lower()

            logging.info('Selected: {}'.format(decision))
            if decision == 'n':
                break;
            elif decision == 'r':
                continue
            else:
                # User chose 'y'. Proceed with the merge.
                logging.info('Merging pending QC files to positive/negative master set...')
                tmp_merged_positive_file_path = autolabeled_positive_records_file_path + '.tmp'
                sharedlib.merge_files([autolabeled_positive_records_file_path, autolabeled_positive_records_pending_qc_file_path], tmp_merged_positive_file_path)
                shutil.move(tmp_merged_positive_file_path, autolabeled_positive_records_file_path)

                tmp_merged_negative_file_path = autolabeled_negative_records_file_path + '.tmp'
                sharedlib.merge_files([autolabeled_negative_records_file_path, autolabeled_negative_records_pending_qc_file_path], tmp_merged_negative_file_path)
                shutil.move(tmp_merged_negative_file_path, autolabeled_negative_records_file_path)

                total_autolabeled_positive_records = get_total_lines_count(autolabeled_positive_records_file_path) if os.path.exists(autolabeled_positive_records_file_path) else 0
                total_autolabeled_negative_records = get_total_lines_count(autolabeled_negative_records_file_path) if os.path.exists(autolabeled_negative_records_file_path) else 0

                logging.info('Files merged. Total {} positive and {} negative records in autolabeled master set.'.format(total_autolabeled_positive_records, total_autolabeled_negative_records))
                break;