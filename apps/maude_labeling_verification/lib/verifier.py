import os
from azure.storage.blob import BlockBlobService

import config
import util
import util_azure


def build_potential_file_sets(input_files,  potential_positive_records_file, potential_negative_records_file):
    print('Building potential positive and negative files...')

    input_dir = util.fix_path(config.input_dir)

    with open(potential_positive_records_file, 'w', encoding='utf-8', errors='ignore') as consolidated_pos:
        with open(potential_negative_records_file, 'w', encoding='utf-8', errors='ignore') as consolidated_neg:
            for input_data_file_set in input_files:
                positive_records_file = os.path.join(input_dir, input_data_file_set['positive_records_file'])
                negative_records_file = os.path.join(input_dir, input_data_file_set['negative_records_file'])
                if input_data_file_set['always_download'] == True or os.path.exists(positive_records_file) == False or os.path.exists(negative_records_file) == False:
                    print('Auto-labeled archive for {} needs to be downloaded.'.format(input_data_file_set['name']))
                    download_zip_file_path = os.path.join(input_dir, input_data_file_set['name'] + '.zip')
                    util_azure.download_file(input_data_file_set['labeled_archive_url'], download_zip_file_path)
                    print('Extracting auto-labeled archive...')
                    util.unzip(download_zip_file_path, input_dir)
                    print('Auto-labeled files extracted.')
                print('Merging {} into {}...'.format(input_data_file_set['positive_records_file'], potential_positive_records_file))
                fin = open(positive_records_file, encoding='utf-8', errors='ignore')
                for record in fin:
                    if len(record.strip()) == 0:
                        continue
                    consolidated_pos.write(record)

                print('Merging {} into {}...'.format(input_data_file_set['negative_records_file'], potential_negative_records_file))
                fin = open(negative_records_file, encoding='utf-8', errors='ignore')
                for record in fin:
                    if len(record.strip()) == 0:
                        continue
                    consolidated_neg.write(record)


def verify_labels(mode):
    input_files = config.input_data_file_sets
    print('Verifying known positive and negative records from {} file(s)...'.format(len(input_files)))

    potential_positive_records_file = util.fix_path(config.output_files['potential_positive_records_file'])
    potential_negative_records_file = util.fix_path(config.output_files['potential_negative_records_file'])
    positive_records_output_file = util.fix_path(config.output_files['verified_positive_records_file'])
    negative_records_output_file = util.fix_path(config.output_files['verified_negative_records_file'])
    last_processed_record_number_file = util.fix_path(config.output_files['last_processed_record_number_file'])
   
    existing_work_in_progress = util_azure.all_work_in_progress_files_present_on_cloud(config.cloud_files)
    if existing_work_in_progress:
        # Cloud does not have work in progress
        util_azure.download_cloud_files(config.cloud_files, config.output_files)
    else:
        # No cloud files or incomplete set. Create new using data files.
        build_potential_file_sets(input_files, potential_positive_records_file, potential_negative_records_file)


    verify(mode, potential_positive_records_file, potential_negative_records_file, positive_records_output_file, negative_records_output_file, last_processed_record_number_file)
    
    if config.upload_output_to_cloud == True:                            
        print('Upload output{}? [y/n] '.format( '' if existing_work_in_progress else ' (POTENTIALLY OVERWRITE CLOUD)'))
        upload_confirmation = util.get_char_input()
        if not isinstance(upload_confirmation, str):
            upload_confirmation = bytes.decode(upload_confirmation)
        if upload_confirmation == 'y':
            files_to_upload = [positive_records_output_file, negative_records_output_file, last_processed_record_number_file]

            if not existing_work_in_progress:
                files_to_upload += [potential_positive_records_file, potential_negative_records_file]

            util_azure.upload_files(files_to_upload, config.cloud_files['container'])


def verify(mode, potential_positive_records_file, potential_negative_records_file, positive_records_output_file, negative_records_output_file, last_processed_record_number_file):
    last_read_potential_positive_record_number = 0
    last_read_potential_negative_record_number = 0

    if os.path.exists(last_processed_record_number_file):
        print('Reading the last processed record number...')
        with open(last_processed_record_number_file, 'r') as f:
            for line in f:
                line_lower = line.lower()
                if 'pos' in line_lower:
                    last_read_potential_positive_record_number = int(line.replace('pos:', ''))
                elif 'neg' in line_lower:
                    last_read_potential_negative_record_number = int(line.replace('neg:', ''))


    input_file = potential_positive_records_file
    last_read_record_number = last_read_potential_positive_record_number
    if mode.lower() == 'neg':
        input_file = potential_negative_records_file
        last_read_record_number = last_read_potential_negative_record_number

    with open(positive_records_output_file, 'a', encoding='utf-8', errors='ignore') as positive_records:
        with open(negative_records_output_file, 'a', encoding='utf-8', errors='ignore') as negative_records:
            input_file_path = util.fix_path(input_file)
            with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_record_number = 0
                for line in f:
                    current_record_number += 1
                    if current_record_number <= last_read_record_number:
                        continue

                    print ('')
                    print('Input File: {}'.format(os.path.basename(input_file_path)))
                    print('Output File (positive): {}'.format(os.path.basename(positive_records_output_file)))
                    print('Output File (negative): {}'.format(os.path.basename(negative_records_output_file)))
                    print('Record Number: {}'.format(current_record_number))
                    print ('')
                    print(line)
                    print ('')
                    print('[P]ositive, [N]egative, [U]nknown or [Q]uit? ')
                    decision = util.get_char_input()
                    if not isinstance(decision, str):
                        decision = bytes.decode(decision)

                    if decision == 'q' or decision == 'quit':
                        return

                    if decision == 'p' or decision == 'positive':
                        print('Selected: Positive')
                        positive_records.write(line)
                    elif decision == 'n' or decision == 'negative':
                        print('Selected: Negative')
                        negative_records.write(line)
                    else:
                        print('Selected: Unknown')

                    last_read_record_number = current_record_number
                    if mode.lower() == 'pos':
                        last_read_potential_positive_record_number = last_read_record_number
                    else:
                        last_read_potential_negative_record_number = last_read_record_number

                    with open(last_processed_record_number_file, 'w') as last_processed:
                        last_processed.write('pos:' + str(last_read_potential_positive_record_number))
                        last_processed.write('neg:' + str(last_read_potential_negative_record_number))
