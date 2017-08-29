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

def download_models_from_cloud(models_config, output_dir):
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

    models = download_models_from_cloud(config.models, config.models_output_dir)

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
    print('Reading the already processed record numbers...')
    if not os.path.exists(file_path):
        return {}

    with open(file_path, 'r') as f:
        return json.load(f)

def save_already_read_records(file_path, json_data):
    print('Saving already processed record numbers...')
    with open(file_path, 'w') as f:
        f.write(json.dumps(json_data, indent=4))

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count

def get_unique_random_record_number(total_potential_positive_records, already_read_record_numbers):
   all_possible = set(range(1, total_potential_positive_records+1))
   already_read = set(already_read_record_numbers.keys())
   eligible_record_numbers = all_possible.difference(already_read)
   
   choice = random.choice(list(eligible_record_numbers))
   print('All possible in this file: {}, already read: {} eligible: {}, randomly selected: {}'.format(len(all_possible), len(already_read), len(eligible_record_numbers), choice))
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
        already_read_records[potential_positive_records_file_basename] = []

    if not potential_negative_records_file_basename in already_read_records:
        already_read_records[potential_negative_records_file_basename] = []

    if not questionable_positive_records_file_basename in already_read_records:
        already_read_records[questionable_positive_records_file_basename] = []

    if not questionable_negative_records_file_basename in already_read_records:
        already_read_records[questionable_negative_records_file_basename] = []

    verified_positive_records_file_path = util.fix_path(config.output_files['verified_positive_records_file'])
    verified_negative_records_file_path = util.fix_path(config.output_files['verified_negative_records_file'])

    total_verified_positive_records = get_total_lines_count(verified_positive_records_file_path)
    total_verified_negative_records = get_total_lines_count(verified_negative_records_file_path)

    total_new_records_labeled_this_session = 0
    total_new_records_labeled_using_current_models = 0
    model_accuracy_counts = {}

    verified_positive_records_file = open(verified_positive_records_file_path, 'a+', encoding='utf-8', errors='ignore')
    verified_negative_records_file = open(verified_negative_records_file_path, 'a+', encoding='utf-8', errors='ignore')

    while True:
        if config.auto_regen_models == True and total_new_records_labeled_using_current_models >= config.models_auto_regen_records_threshold:
            print('Models need to re regenerated because {} records have been labeled in this session without models regenerated.'.format(total_new_records_labeled_using_current_models))
            bulk_close_files([verified_positive_records_file, verified_negative_records_file])
            new_models = rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
            output_files = bulk_open_files([verified_positive_records_file_path, verified_negative_records_file_path], 'a+')
            verified_positive_records_file = output_files[0]
            verified_negative_records_file = output_files[1]
            if new_models is not None:
                models = new_models
                total_new_records_labeled_using_current_models = 0

        print ('-------------------------------------------------------------------')
        file_to_read_basename = mode if mode is not None else random.choice([key for key in already_read_records])
        print ('So far => POS: {}, NEG: {}. Next file to look at: {}. Number of records before models auto re-generated: {}'.format(total_verified_positive_records, total_verified_negative_records, file_to_read_basename, config.models_auto_regen_records_threshold - total_new_records_labeled_using_current_models))
        file_to_read = None
        aleady_read_record_numbers = already_read_records[file_to_read_basename]
        record_number_to_read = get_unique_random_record_number(total_available_records[file_to_read_basename],
                                                                aleady_read_record_numbers)
        file_to_read = input_file_basename_to_full_path_map[file_to_read_basename]

        print('Input File: {}'.format(os.path.basename(file_to_read)))
        print('Record Number: {}'.format(record_number_to_read))
        line = get_line(file_to_read, record_number_to_read)
        print ('')
        print(line)
        print ('')
        print ('SUGGESTIONS:')
        suggestions = []
        suggestions.append(get_label_from_filename(file_to_read_basename))
        print ('    Per pre-labeling: {}'.format(suggestions[0]))
        classification_results = []
        if len(models) > 0:
            classification_results = classify(line, models)
            for (model_name, result) in classification_results:
                suggestions.append(result)
                accuracy = model_accuracy_counts[model_name] / total_new_records_labeled_this_session if model_name in model_accuracy_counts and total_new_records_labeled_this_session > 0 else 0
                print('    Per {} (Accuracy {:}%): {}'.format(model_name, round(accuracy * 100, 2), result.upper()))
        else:
            print ('    No trained model available to provide a suggestion.')

        print ('Likely: {}'.format(get_likely_suggestion(suggestions)))

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
            bulk_close_files([verified_positive_records_file, verified_negative_records_file])
            new_models = rebuild_models(verified_positive_records_file_path, verified_negative_records_file_path, already_processed_record_numbers_file)
            output_files = bulk_open_files([verified_positive_records_file_path, verified_negative_records_file_path], 'a+')
            verified_positive_records_file = output_files[0]
            verified_negative_records_file = output_files[1]
            if new_models is not None:
                models = new_models
                total_new_records_labeled_using_current_models = 0
            continue;
        elif decision == 'p':
            print('Selected: Positive')
            verified_positive_records_file.write(line)
            total_verified_positive_records += 1
            total_new_records_labeled_using_current_models += 1
            total_new_records_labeled_this_session += 1
            if not record_number_to_read in already_read_records:
                aleady_read_record_numbers[record_number_to_read] = []
            aleady_read_record_numbers[record_number_to_read].append({line[:40]: 'pos'})
        elif decision == 'n':
            print('Selected: Negative')
            verified_negative_records_file.write(line)
            total_verified_negative_records += 1
            total_new_records_labeled_using_current_models += 1
            total_new_records_labeled_this_session += 1
            if not record_number_to_read in already_read_records:
                aleady_read_record_numbers[record_number_to_read] = []
            aleady_read_record_numbers[record_number_to_read].append({line[:40]: 'neg'})
        else:
            total_new_records_labeled_using_current_models += 1
            print('Selected: Unknown')

        for (model_name, result) in classification_results:
            if decision == 'p' and result.lower() == 'pos':
                model_accuracy_counts[model_name] = model_accuracy_counts[model_name] + 1 if model_name in model_accuracy_counts else 1
            elif decision == 'n' and result.lower() == 'neg':
                model_accuracy_counts[model_name] = model_accuracy_counts[model_name] + 1 if model_name in model_accuracy_counts else 1

        save_already_read_records(already_processed_record_numbers_file, already_read_records)

    verified_positive_records_file.close()
    verified_negative_records_file.close()
