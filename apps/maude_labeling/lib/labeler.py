import os
import json
import random
from azure.storage.blob import BlockBlobService

import config
import util
import util_azure


def build_potential_file_sets(input_files,  potential_positive_records_file_merged, potential_negative_records_file_merged, questionable_positive_records_file_merged, questionable_negative_records_file_merged):
    print('Building potential positive and negative files...')

    input_dir = util.fix_path(config.input_dir)

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
                            print('Auto-labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))
                            download_zip_file_path = os.path.join(input_dir, input_data_file_set['name'] + '.zip')
                            util_azure.download_file(input_data_file_set['labeled_archive_url'], download_zip_file_path)
                            print('Extracting auto-labeled archive...')
                            util.unzip(download_zip_file_path, input_dir)
                            print('Auto-labeled files extracted.')
                        print('Merging {} into {}...'.format(input_data_file_set['potential_positive_records_file'], potential_positive_records_file_merged))
                        fin = open(potential_positive_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_pos.write(record)

                        print('Merging {} into {}...'.format(input_data_file_set['potential_negative_records_file'], potential_negative_records_file_merged))
                        fin = open(potential_negative_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_neg.write(record)

                        print('Merging {} into {}...'.format(input_data_file_set['questionable_positive_records_file'], questionable_positive_records_file_merged))
                        fin = open(questionable_positive_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_questionable_pos.write(record)

                        print('Merging {} into {}...'.format(input_data_file_set['questionable_negative_records_file'], questionable_negative_records_file_merged))
                        fin = open(questionable_negative_records_file, encoding='utf-8', errors='ignore')
                        for record in fin:
                            if len(record.strip()) == 0:
                                continue
                            consolidated_questionable_neg.write(record)

def label_records(mode):
    input_files = config.input_data_file_sets
    print('Labeling known positive and negative records from {} file(s)...'.format(len(input_files)))

    potential_positive_records_file = util.fix_path(config.output_files['potential_positive_records_file'])
    questionable_positive_records_file = util.fix_path(config.output_files['questionable_positive_records_file'])
    potential_negative_records_file = util.fix_path(config.output_files['potential_negative_records_file'])
    questionable_negative_records_file = util.fix_path(config.output_files['questionable_negative_records_file'])
 
    positive_records_output_file = util.fix_path(config.output_files['verified_positive_records_file'])
    negative_records_output_file = util.fix_path(config.output_files['verified_negative_records_file'])
    already_processed_record_numbers_file = util.fix_path(config.output_files['already_processed_record_numbers_file'])
   
    existing_work_in_progress = util_azure.all_work_in_progress_files_present_on_cloud(config.cloud_files)
    if existing_work_in_progress:
        # Cloud does not have work in progress
        util_azure.download_cloud_files(config.cloud_files, config.output_files)
    else:
        # No cloud files or incomplete set. Create new using data files.
        build_potential_file_sets(input_files, potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file)

    label(mode, potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file)
    
    if config.upload_output_to_cloud == True:                            
        print('Upload output{}? [y/n] '.format( '' if existing_work_in_progress else ' (POTENTIALLY OVERWRITE CLOUD)'))
        upload_confirmation = util.get_char_input()
        if not isinstance(upload_confirmation, str):
            upload_confirmation = bytes.decode(upload_confirmation)
        if upload_confirmation == 'y':
            files_to_upload = [positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file]

            if not existing_work_in_progress:
                files_to_upload += [potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file]

            util_azure.upload_files(files_to_upload, config.cloud_files['container'])


def get_already_read_records(file_path):
    print('Reading the last processed record numbers...')
    if not os.path.exists(file_path):
        default_dict = {}
        default_dict['pos'] = []
        default_dict['pos?'] = []
        default_dict['neg'] = []
        default_dict['neg?'] = []
        return default_dict

    with open(file_path, 'r') as f:
        return json.load(f)

def save_already_read_records(file_path, json_data):
    print('Writing the last processed record numbers...')
    with open(file_path, 'w') as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def get_unique_random_record_number(total_potential_positive_records, already_read_record_numbers):
   all_possible = set(range(1, total_potential_positive_records+1))
   already_read = set(already_read_record_numbers)
   eligible_record_numbers = all_possible.difference(already_read)
   
   choice = random.choice(list(eligible_record_numbers))
   print('All possible: {}, already read: {} eligible_record_numbers: {}, choice: {}'.format(len(all_possible), len(already_read), len(eligible_record_numbers), choice))
   return choice

def get_line(file_to_read, record_number_to_read):
    with open(file_to_read, 'r', encoding='utf-8', errors='ignore') as f:
        line_count = 0
        for line in f:
            line_count += 1
            if line_count == record_number_to_read:
                return line
    return 'NO RECORD FOUND AT LINE NUMBER {} IN {}'.format(record_number_to_read, file_to_read)

def label(mode, potential_positive_records_file, potential_negative_records_file,  questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file):
    already_read_records = get_already_read_records(already_processed_record_numbers_file)
    
    total_potential_positive_records = get_total_lines_count(potential_positive_records_file)
    total_potential_negative_records = get_total_lines_count(potential_negative_records_file)
    total_questionable_positive_records = get_total_lines_count(questionable_positive_records_file)
    total_questionable_negative_records = get_total_lines_count(questionable_negative_records_file)

    verified_positive_records_file_path = util.fix_path(config.output_files['verified_positive_records_file'])
    verified_negative_records_file_path = util.fix_path(config.output_files['verified_negative_records_file'])

    total_verified_positive_records = get_total_lines_count(verified_positive_records_file_path)
    total_verified_negative_records = get_total_lines_count(verified_negative_records_file_path)

    with open(verified_positive_records_file_path, 'w', encoding='utf-8', errors='ignore') as positive_records:
        with open(verified_negative_records_file_path, 'w', encoding='utf-8', errors='ignore') as negative_records:
            while True:
                file_type_to_read = mode if mode is not None else random.choice(['pos', 'neg', 'pos?', 'neg?'])
                file_to_read = None
                aleady_read_record_numbers = None
                record_number_to_read = 1

                if file_type_to_read == 'pos':
                    file_to_read = potential_positive_records_file
                    aleady_read_record_numbers = already_read_records['pos']
                    record_number_to_read = get_unique_random_record_number(total_potential_positive_records, aleady_read_record_numbers)
                elif file_type_to_read == 'neg':
                    file_to_read = potential_negative_records_file
                    aleady_read_record_numbers = already_read_records['neg']
                    record_number_to_read = get_unique_random_record_number(total_potential_negative_records, aleady_read_record_numbers)
                elif file_type_to_read == 'pos?':
                    file_to_read = questionable_positive_records_file
                    aleady_read_record_numbers =  already_read_records['pos?']
                    record_number_to_read = get_unique_random_record_number(total_questionable_positive_records, aleady_read_record_numbers)
                elif file_type_to_read == 'neg?':
                    file_to_read = questionable_negative_records_file
                    aleady_read_record_numbers = already_read_records['neg?']
                    record_number_to_read = get_unique_random_record_number(total_questionable_negative_records, aleady_read_record_numbers)

                line = get_line(file_to_read, record_number_to_read)

                print ('')
                print ('So far => POS: {}, NEG: {}'.format(total_verified_positive_records, total_verified_negative_records))
                print('Input File: {}'.format(os.path.basename(file_to_read)))
                print('Record Number: {}'.format(record_number_to_read))
                print(line)
                print ('')
                print ('SUGGESTION: {}'.format(file_type_to_read.upper()))
                print('[P]ositive, [N]egative, [U]nknown or [Q]uit? ')
                print ('')
                decision = util.get_char_input()
                if not isinstance(decision, str):
                    decision = bytes.decode(decision)

                decision = decision.lower()
                if decision == 'q':
                    print('Selected: Quit')
                    break;
                elif decision == 'p':
                    print('Selected: Positive')
                    positive_records.write(line)
                    total_verified_positive_records += 1
                    aleady_read_record_numbers.append(record_number_to_read)
                elif decision == 'n':
                    print('Selected: Negative')
                    negative_records.write(line)
                    total_verified_negative_records += 1
                    aleady_read_record_numbers.append(record_number_to_read)
                else:
                    print('Selected: Unknown')
        
                save_already_read_records(already_processed_record_numbers_file, already_read_records)
