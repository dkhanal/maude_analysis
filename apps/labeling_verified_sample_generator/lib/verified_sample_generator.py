# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import json
import random
import logging
import datetime
import re

from azure.storage.blob import BlockBlobService

import sharedlib
import config


import __remote_server_helper
import __modeling_helper
import __classification_helper

def build_potential_file_sets(input_files,  potential_positive_records_file_merged, potential_negative_records_file_merged, questionable_positive_records_file_merged, questionable_negative_records_file_merged):
    logging.info('Building potential positive and negative files...')

    input_dir = sharedlib.abspath(config.input_dir)

    with open(potential_positive_records_file_merged, 'w', encoding='utf-8', errors='ignore') as consolidated_pos:
        with open(potential_negative_records_file_merged, 'w', encoding='utf-8', errors='ignore') as consolidated_neg:
            with open(questionable_positive_records_file_merged, 'w', encoding='utf-8', errors='ignore') as consolidated_questionable_pos:
                with open(questionable_negative_records_file_merged, 'w', encoding='utf-8', errors='ignore') as consolidated_questionable_neg:
                    for input_data_file_set in input_files:
                        potential_positive_records_file = os.path.join(input_dir, input_data_file_set['potential_positive_records_file'])
                        potential_negative_records_file = os.path.join(input_dir, input_data_file_set['potential_negative_records_file'])
                        questionable_positive_records_file = os.path.join(input_dir, input_data_file_set['questionable_positive_records_file'])
                        questionable_negative_records_file = os.path.join(input_dir, input_data_file_set['questionable_negative_records_file'])
                        if input_data_file_set['always_download'] == True or os.path.exists(potential_positive_records_file) == False or os.path.exists(potential_negative_records_file) == False:
                            logging.info('Pre-labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))

                            prelabeled_file_url = sharedlib.join_remote_server_paths(config.remote_server['base_uri'], config.remote_server['labeling_candidates_dir'], input_data_file_set['prelabeled_archive_name'])

                            download_zip_file_path = os.path.join(input_dir, input_data_file_set['name'] + '.zip')
                            sharedlib.download_file(prelabeled_file_url, download_zip_file_path)
                            logging.info('Extracting auto-labeled archive...')
                            sharedlib.unzip(download_zip_file_path, input_dir)
                            logging.info('Pre-labeled files extracted.')
                        logging.info('Merging {} into {}...'.format(input_data_file_set['potential_positive_records_file'], potential_positive_records_file_merged))
                        fin = open(potential_positive_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_pos.write(record)

                        logging.info('Merging {} into {}...'.format(input_data_file_set['potential_negative_records_file'], potential_negative_records_file_merged))
                        fin = open(potential_negative_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_neg.write(record)

                        logging.info('Merging {} into {}...'.format(input_data_file_set['questionable_positive_records_file'], questionable_positive_records_file_merged))
                        fin = open(questionable_positive_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_questionable_pos.write(record)

                        logging.info('Merging {} into {}...'.format(input_data_file_set['questionable_negative_records_file'], questionable_negative_records_file_merged))
                        fin = open(questionable_negative_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_questionable_neg.write(record)

def label_records(mode):
    input_files = config.input_data_file_sets
    logging.info('Labeling known positive and negative records from {} file(s)...'.format(len(input_files)))

    potential_positive_records_file = sharedlib.abspath(config.output_files['potential_positive_records_file'])
    questionable_positive_records_file = sharedlib.abspath(config.output_files['questionable_positive_records_file'])
    potential_negative_records_file = sharedlib.abspath(config.output_files['potential_negative_records_file'])
    questionable_negative_records_file = sharedlib.abspath(config.output_files['questionable_negative_records_file'])
 
    positive_records_output_file = sharedlib.abspath(config.output_files['verified_positive_records_file'])
    negative_records_output_file = sharedlib.abspath(config.output_files['verified_negative_records_file'])
    already_processed_record_numbers_file = sharedlib.abspath(config.output_files['already_processed_record_numbers_file'])
   
    existing_work_in_progress = __remote_server_helper.all_work_in_progress_files_present_on_remote_server(config.remote_server, config.remote_server_files)
    if existing_work_in_progress:
        __remote_server_helper.download_remote_server_files(config.remote_server, config.remote_server_files, config.output_files)
    else:
        # No cloud files or incomplete set. Create new using data files.
        build_potential_file_sets(input_files, potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file)

    models = __remote_server_helper.download_models_from_remote_server(config.remote_server, config.models, config.models_output_dir)

    label(mode, potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file, models)
    
    sharedlib.remove_duplicate_records([positive_records_output_file, negative_records_output_file])

    if config.upload_output_to_remote_server == True:
        logging.info('Upload output{}? [y/n] '.format( '' if existing_work_in_progress else ' (POTENTIALLY OVERWRITE CLOUD)'))
        upload_confirmation = sharedlib.get_char_input()
        if not isinstance(upload_confirmation, str):
            upload_confirmation = bytes.decode(upload_confirmation)
        if upload_confirmation == 'y':
            files_to_upload = [positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file]
            accuracy_file_pattern = re.compile('.*_accuracy.json')
            accuarcy_files = [sharedlib.abspath(os.path.join(config.output_dir, file_name)) for file_name in os.listdir(config.output_dir) if re.search(accuracy_file_pattern, file_name) is not None]
    
            files_to_upload += accuarcy_files


            if not existing_work_in_progress:
                files_to_upload += [potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file]

            sharedlib.upload_files_to_remote_server(files_to_upload, config.remote_server[labeling_verified_samples_dir'])


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
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    logging.info('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def get_unique_random_record_number(total_potential_positive_records, already_read_record_numbers):
   all_possible = set(range(1, total_potential_positive_records+1))
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

def get_label_from_filename(filename):
    if filename is None:
        return None
    filename_lower = filename.lower()
    if 'potential_positive' in filename_lower:
        return 'POS'

    if 'potential_negative' in filename_lower:
        return 'NEG'

    if 'questionable_positive' in filename_lower:
        return 'POS?'

    if 'questionable_negative' in filename_lower:
        return 'NEG?'

    return 'UNK'

def get_likely_suggestion(suggestions):
    if suggestions is None or len(suggestions) == 0:
        return 'UNK'

    total_suggestions = len(suggestions)
    if len([s for s in suggestions if 'pos' in s.lower()]) >= total_suggestions/2:
        return 'POS'

    if len([s for s in suggestions if 'neg' in s.lower()]) >= total_suggestions/2:
        return 'NEG'

    return 'UNK'

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

def get_labeling_accuracy(model_name, output_dir):
    accuracy_file_path = os.path.join(sharedlib.abspath(output_dir), model_name + '_accuracy.json')
    if not os.path.exists(accuracy_file_path):
        return (0, 0, 0) # Tuple structure is: (<all time accuracy>, <accuracy over last 500>, <accuracy over last 100>)

    with open(accuracy_file_path, 'r') as f:
        accuracy_data = json.load(f)

    if accuracy_data is None: # No previous accuracy info for this model
        return (0, 0, 0)

    total_all_time = len(accuracy_data)
    last_100 = accuracy_data[-100:]
    last_500 = accuracy_data[-500:]
    total_last_100 = len(last_100)
    total_last_500 = len(last_500)

    correct_all_time = len([item for item in accuracy_data if item['correct'] == True])
    correct_last_100 = len([item for item in last_100 if item['correct'] == True])
    correct_last_500 = len([item for item in last_500 if item['correct'] == True])

    return (correct_all_time / total_all_time, correct_last_500 / total_last_500, correct_last_100 / total_last_100)


def save_labeling_accuracy(model_name, output_dir, record_id, classification, is_correct):
    accuracy_file_path = os.path.join(sharedlib.abspath(output_dir), model_name + '_accuracy.json')
    
    accuracy_data = None
    if os.path.exists(accuracy_file_path):
        with open(accuracy_file_path, 'r') as f:
            accuracy_data = json.load(f)

    if accuracy_data is None: # No previous accuracy info for this model
        accuracy_data = []

    item = {}
    item['timestamp'] = datetime.datetime.now().isoformat()
    item['recordid'] = record_id
    item['classification'] = classification
    item['correct'] = is_correct

    accuracy_data.append(item)
    with open(accuracy_file_path, 'w') as f:
        json.dump(accuracy_data, f, indent=4)

def label(mode, potential_positive_records_file, potential_negative_records_file,  questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file, models):
    potential_positive_records_file_basename = os.path.basename(potential_positive_records_file).lower()
    potential_negative_records_file_basename = os.path.basename(potential_negative_records_file).lower()
    questionable_positive_records_file_basename = os.path.basename(questionable_positive_records_file).lower()
    questionable_negative_records_file_basename = os.path.basename(questionable_negative_records_file).lower()

    input_file_basename_to_full_path_map = {}
    input_file_basename_to_full_path_map[potential_positive_records_file_basename] = potential_positive_records_file
    input_file_basename_to_full_path_map[potential_negative_records_file_basename] = potential_negative_records_file
    input_file_basename_to_full_path_map[questionable_positive_records_file_basename] = questionable_positive_records_file
    input_file_basename_to_full_path_map[questionable_negative_records_file_basename] = questionable_negative_records_file

    already_read_records = get_already_read_records(already_processed_record_numbers_file)
    if already_read_records is None or len(already_read_records) == 0:
        already_read_records = {}

    total_available_records = {}
    total_available_records[potential_positive_records_file_basename] = get_total_lines_count(potential_positive_records_file)
    total_available_records[potential_negative_records_file_basename] = get_total_lines_count(potential_negative_records_file)
    total_available_records[questionable_positive_records_file_basename] = get_total_lines_count(questionable_positive_records_file)
    total_available_records[questionable_negative_records_file_basename] = get_total_lines_count(questionable_negative_records_file)

    if not potential_positive_records_file_basename in already_read_records:
        already_read_records[potential_positive_records_file_basename] = {}

    if not potential_negative_records_file_basename in already_read_records:
        already_read_records[potential_negative_records_file_basename] = {}

    if not questionable_positive_records_file_basename in already_read_records:
        already_read_records[questionable_positive_records_file_basename] = {}

    if not questionable_negative_records_file_basename in already_read_records:
        already_read_records[questionable_negative_records_file_basename] = {}

    verified_positive_records_file_path = sharedlib.abspath(config.output_files['verified_positive_records_file'])
    verified_negative_records_file_path = sharedlib.abspath(config.output_files['verified_negative_records_file'])

    total_verified_positive_records = get_total_lines_count(verified_positive_records_file_path) if os.path.exists(verified_positive_records_file_path) else 0
    total_verified_negative_records = get_total_lines_count(verified_negative_records_file_path) if os.path.exists(verified_negative_records_file_path) else 0

    total_new_records_labeled_this_session = 0
    total_new_records_labeled_using_current_models = 0
    model_accuracy_counts = {}

    verified_positive_records_file = open(verified_positive_records_file_path, 'a+', encoding='utf-8', errors='ignore')
    verified_negative_records_file = open(verified_negative_records_file_path, 'a+', encoding='utf-8', errors='ignore')

    while True:
        if config.auto_regen_models == True and total_new_records_labeled_using_current_models >= config.models_auto_regen_records_threshold:
            logging.info('Models need to re regenerated because {} records have been labeled in this session without models regenerated.'.format(total_new_records_labeled_using_current_models))
            bulk_close_files([verified_positive_records_file, verified_negative_records_file])
            new_models = __modeling_helper.rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
            output_files = bulk_open_files([verified_positive_records_file_path, verified_negative_records_file_path], 'a+')
            verified_positive_records_file = output_files[0]
            verified_negative_records_file = output_files[1]
            if new_models is not None:
                models = new_models
                total_new_records_labeled_using_current_models = 0

        logging.info('-------------------------------------------------------------------')
        file_to_read_basename = mode if mode is not None else random.choice([key for key in already_read_records])

        if file_to_read_basename == 'pos':
            file_to_read_basename = potential_positive_records_file_basename
        elif file_to_read_basename == 'neg':
            file_to_read_basename = potential_negative_records_file_basename
        elif file_to_read_basename == 'pos?':
            file_to_read_basename = questionable_positive_records_file_basename
        elif file_to_read_basename == 'neg?':
            file_to_read_basename = questionable_negative_records_file_basename

        logging.info('So far => POS: {}, NEG: {}. Next file to look at: {}. Number of records before models auto re-generated: {}'.format(total_verified_positive_records, total_verified_negative_records, file_to_read_basename, config.models_auto_regen_records_threshold - total_new_records_labeled_using_current_models))
        file_to_read = None
        aleady_read_record_numbers = already_read_records[file_to_read_basename]
        record_number_to_read = get_unique_random_record_number(total_available_records[file_to_read_basename],
                                                                aleady_read_record_numbers)
        file_to_read = input_file_basename_to_full_path_map[file_to_read_basename]

        logging.info('Input File: {}'.format(os.path.basename(file_to_read)))
        logging.info('Record Number: {}'.format(record_number_to_read))
        line = get_line(file_to_read, record_number_to_read)
        line_id = line[:40]
        logging.info('')
        logging.info(line)
        logging.info('')
        logging.info('SUGGESTIONS:')
        suggestions = []
        suggestions.append(get_label_from_filename(file_to_read_basename))
        logging.info('    Per pre-labeling: {}'.format(suggestions[0]))
        classification_results = []
        overall_suggestion_model_name = 'overall.decision_support'
        overall_suggestion = None
        if len(models) > 0:
            classification_results = __classification_helper.classify(line, models) # returns tuple: (name, (predicted_classification, positive_proba))
            for (model_name, result) in classification_results:
                suggestions.append(result[0])
                accuracy = get_labeling_accuracy(model_name, sharedlib.abspath(config.output_dir))
                logging.info('    Per {} (Past accuracy {:}%/{:}%/{:}%): {}'.format(model_name, round(accuracy[0] * 100, 2), round(accuracy[1] * 100, 2), round(accuracy[2] * 100, 2), result[0].upper()))
        else:
            logging.info('    No trained model available to provide a suggestion.')

        overall_suggestion_accuracy = get_labeling_accuracy(overall_suggestion_model_name, sharedlib.abspath(config.output_dir))
        overall_suggestion = get_likely_suggestion(suggestions)
        logging.info('OVERALL (Past accuracy {:}%/{:}%/{:}%): {}'.format(round(overall_suggestion_accuracy[0] * 100, 2), round(overall_suggestion_accuracy[1] * 100, 2), round(overall_suggestion_accuracy[2] * 100, 2), overall_suggestion))

        logging.info('')
        logging.info('[P]ositive, [N]egative, [U]nknown, [R]ebuild Models or [Q]uit? ')
        logging.info('')

        decision = None
        while (decision != 'q' and decision != 'r' and decision != 'p' and decision != 'n' and decision != 'u'):
            decision = sharedlib.get_char_input()
            if not isinstance(decision, str):
                decision = bytes.decode(decision)
            decision = decision.lower()

        if decision == 'q':
            logging.info('Selected: Quit')
            break;
        elif decision == 'r':
            logging.info('Selected: Rebuild models')
            bulk_close_files([verified_positive_records_file, verified_negative_records_file])
            new_models = __modeling_helper.rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
            output_files = bulk_open_files([verified_positive_records_file_path, verified_negative_records_file_path], 'a+')
            verified_positive_records_file = output_files[0]
            verified_negative_records_file = output_files[1]
            if new_models is not None:
                models = new_models
                total_new_records_labeled_using_current_models = 0
            continue;
        elif decision == 'p':
            logging.info('Selected: Positive')
            verified_positive_records_file.write(line)
            total_verified_positive_records += 1
            total_new_records_labeled_using_current_models += 1
            total_new_records_labeled_this_session += 1
            if not record_number_to_read in already_read_records:
                aleady_read_record_numbers[record_number_to_read] = []
            aleady_read_record_numbers[record_number_to_read].append({line_id: 'pos'})
        elif decision == 'n':
            logging.info('Selected: Negative')
            verified_negative_records_file.write(line)
            total_verified_negative_records += 1
            total_new_records_labeled_using_current_models += 1
            total_new_records_labeled_this_session += 1
            if not record_number_to_read in already_read_records:
                aleady_read_record_numbers[record_number_to_read] = []
            aleady_read_record_numbers[record_number_to_read].append({line_id: 'neg'})
        else:
            total_new_records_labeled_using_current_models += 1
            logging.info('Selected: Unknown')

        for (model_name, result) in classification_results: # result is a tuple: (predicted_classification, predicted_proba)
            is_correct = False
            if decision == 'p' and result[0].lower() == 'pos':
                is_correct = True
            elif decision == 'n' and result[0].lower() == 'neg':
                is_correct = True

            save_labeling_accuracy(model_name, os.path.dirname(verified_positive_records_file_path), line_id, result[0], is_correct)

        if overall_suggestion is not None:
            if (decision == 'p' and overall_suggestion.lower() == 'pos') or (decision == 'n' and overall_suggestion.lower() == 'neg') :
                save_labeling_accuracy(overall_suggestion_model_name, sharedlib.abspath(config.output_dir), line_id,
                                       overall_suggestion, True)
            else:
                save_labeling_accuracy(overall_suggestion_model_name, sharedlib.abspath(config.output_dir), line_id,
                                       overall_suggestion, False)

        save_already_read_records(already_processed_record_numbers_file, already_read_records)

    verified_positive_records_file.close()
    verified_negative_records_file.close()