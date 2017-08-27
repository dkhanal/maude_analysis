import os
import json
import random
from azure.storage.blob import BlockBlobService

import config
import util
import util_azure
import modeler
import classifier

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

def build_models_from_cloud(models_config, output_dir):
    print('Downloading models...')
    output_dir = util.fix_path(output_dir)
    block_blob_service = BlockBlobService(config.azure_account_name, config.azure_account_key)
    blobs = [item.name for item in block_blob_service.list_blobs(config.models_cloud_blob_container_name)]

    models = []
    for model_config in models_config:
        name_zip_tuple = (model_config['name'], model_config['name'] + '.zip', os.path.join(output_dir, model_config['name'] + '.zip'))
        if name_zip_tuple[1] in blobs:
            util_azure.download_file(model_config['remote_url'], name_zip_tuple[2])
            util.unzip(name_zip_tuple[2], output_dir)
            pickle_file = os.path.join(output_dir, name_zip_tuple[0] + '.pickle')
            if os.path.exists(pickle_file):
                model = util.load_pickle(pickle_file)
                models.append((name_zip_tuple[0], model))
        else:
            print('Could not find model file {} on the Cloud'.format( name_zip_tuple[1]))

    print ('{} MODELS LOADED'.format(len(models)))
    return models

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

    models = build_models_from_cloud(config.models, config.models_output_dir)

    label(mode, potential_positive_records_file, potential_negative_records_file, questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file, models)
    
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
    print('Saving already processed record numbers...')
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

def rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file):
    print ('Rebuilding models...')
    if config.regen_models is None or config.regen_models == False:
        print('Configuration does NOT allow regeneration of the models.')
        return None

    models_config = config.models
    upload_models_to_cloud = config.upload_models_to_cloud
    models_cloud_blob_container_name = config.models_cloud_blob_container_name

    print ('Uploading labeled records so far to Cloud...')
    files_to_upload = [verified_positive_records_file_path, verified_negative_records_file_path,
                       already_processed_record_numbers_file]
    util_azure.upload_files(files_to_upload, config.cloud_files['container'])

    print ('Generating models...')
    model_pickles = modeler.generate_models([verified_positive_records_file_path],
                                            [verified_negative_records_file_path],
                                            models_config,
                                            config.models_output_dir,
                                            upload_models_to_cloud,
                                            models_cloud_blob_container_name,
                                            os.path.join(config.models_output_dir, 'process.log')
                                            )
    models = []

    for model_name_pickle_tuple in model_pickles:
        if os.path.exists(model_name_pickle_tuple[1]):
            model = util.load_pickle(model_name_pickle_tuple[1])
            models.append((model_name_pickle_tuple[0], model))

    print ('*** {} MODELS REBUILT ***'.format(len(models)))
    return models

def classify(line, models):
    if models is None or len(models) == 0:
        return None

    return classifier.classify_record(line, models)

def label(mode, potential_positive_records_file, potential_negative_records_file,  questionable_positive_records_file, questionable_negative_records_file, positive_records_output_file, negative_records_output_file, already_processed_record_numbers_file, models):
    already_read_records = get_already_read_records(already_processed_record_numbers_file)
    
    total_potential_positive_records = get_total_lines_count(potential_positive_records_file)
    total_potential_negative_records = get_total_lines_count(potential_negative_records_file)
    total_questionable_positive_records = get_total_lines_count(questionable_positive_records_file)
    total_questionable_negative_records = get_total_lines_count(questionable_negative_records_file)

    verified_positive_records_file_path = util.fix_path(config.output_files['verified_positive_records_file'])
    verified_negative_records_file_path = util.fix_path(config.output_files['verified_negative_records_file'])

    total_verified_positive_records = get_total_lines_count(verified_positive_records_file_path)
    total_verified_negative_records = get_total_lines_count(verified_negative_records_file_path)

    total_new_records_labeled_using_current_models = 0

    with open(verified_positive_records_file_path, 'a', encoding='utf-8', errors='ignore') as positive_records:
        with open(verified_negative_records_file_path, 'a', encoding='utf-8', errors='ignore') as negative_records:
            while True:
                if config.auto_regen_models == True and total_new_records_labeled_using_current_models >= config.models_auto_regen_records_threshold:
                    print('Models need to ge regenerated because {} records have been labeled in this session without models regenerated.'.format(total_new_records_labeled_using_current_models))
                    new_models = rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
                    if new_models is not None:
                        models = new_models
                        total_new_records_labeled_using_current_models = 0

                print ('-------------------------------------------------------------------')
                file_type_to_read = mode if mode is not None else random.choice(['pos', 'neg', 'pos?', 'neg?'])
                print ('So far => POS: {}, NEG: {}. Next record type to look at: {}. Number of records before models auto re-generated: {}'.format(total_verified_positive_records, total_verified_negative_records, file_type_to_read.upper(), config.models_auto_regen_records_threshold - total_new_records_labeled_using_current_models))
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

                print('Input File: {}'.format(os.path.basename(file_to_read)))
                print('Record Number: {}'.format(record_number_to_read))
                line = get_line(file_to_read, record_number_to_read)
                print ('')
                print(line)
                print ('')
                print ('SUGGESTIONS:')
                print ('Per pre-Labeling: {}'.format(file_type_to_read.upper()))
                classification_results = classify(line, models)
                for (model_name, result) in classification_results:
                    print('Per {}: {}'.format(model_name, result.upper()))

                print ('')
                print('[P]ositive, [N]egative, [U]nknown, [R]ebuild Models or [Q]uit? ')
                print ('')
                decision = util.get_char_input()
                if not isinstance(decision, str):
                    decision = bytes.decode(decision)

                decision = decision.lower()
                if decision == 'q':
                    print('Selected: Quit')
                    break;
                elif decision == 'r':
                    print('Selected: Rebuild models')
                    positive_records.flush()
                    negative_records.flush()
                    new_models = rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
                    if new_models is not None:
                        models = new_models
                        total_new_records_labeled_using_current_models = 0
                    continue;
                elif decision == 'p':
                    print('Selected: Positive')
                    positive_records.write(line)
                    total_verified_positive_records += 1
                    total_new_records_labeled_using_current_models += 1
                    aleady_read_record_numbers.append(record_number_to_read)
                elif decision == 'n':
                    print('Selected: Negative')
                    negative_records.write(line)
                    total_verified_negative_records += 1
                    total_new_records_labeled_using_current_models += 1
                    aleady_read_record_numbers.append(record_number_to_read)
                else:
                    total_new_records_labeled_using_current_models += 1
                    print('Selected: Unknown')
        
                save_already_read_records(already_processed_record_numbers_file, already_read_records)
