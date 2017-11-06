# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import re
import sys
import codecs
import datetime
import multiprocessing
import random
import shutil
import logging
import math
import platform

import sharedlib
import config

def split_file(large_file, split_dir, max_records_per_file=50000):
    logging.info('Splitting file {} into mutiple files with max {} records each'.format(large_file, max_records_per_file))
    input_file = sharedlib.abspath(large_file)
    split_dir = sharedlib.abspath(split_dir)
    input_file_base_name = os.path.basename(input_file)

    chunk_number = 0
    line_number = 0
    output_file = None
    chunks = []
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line_number == 0 or line_number == max_records_per_file:
                # Reset
                line_number = 0 
                chunk_number += 1
                if output_file is not None:
                    output_file.close()
                input_file_name_without_ext = os.path.splitext(input_file_base_name)[0]
                chunk_path = os.path.join(split_dir, input_file_name_without_ext + '.{:02d}.txt'.format(chunk_number))
                logging.info('Creating new file: {}...'.format(chunk_path))
                output_file = open(chunk_path, 'w', encoding='utf-8', errors='ignore')
                chunks.append(chunk_path)

            line_number += 1            
            output_file.write(line)

    logging.info('{} split into {} smaller files.'.format(input_file_base_name, len(chunks)))
    output_file.close()
    return chunks

def merge_file_sets(file_base_name, out_dir, positive_files, negative_files, maybe_positive_files, maybe_negative_files, process_log_files):
    output_dir = sharedlib.abspath(out_dir)
    file_name_without_ext = os.path.splitext(file_base_name)[0]
    positive_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.potential_pos.txt')
    negative_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.potential_neg.txt')
    maybe_positive_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.questionable_pos.txt')
    maybe_negative_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.questionable_neg.txt')
    process_log_file =  os.path.join(output_dir,  file_name_without_ext + '.process.txt')

    logging.info('Merging {} positive labeled files into: {}...'.format(len(positive_files), positive_records_output_file))
    merge_files(positive_files, positive_records_output_file)
    logging.info('Merging {} negative labeled files into: {}...'.format(len(negative_files), negative_records_output_file))
    merge_files(negative_files, negative_records_output_file)
    logging.info('Merging {} maybe positive labeled files into: {}...'.format(len(maybe_positive_files), maybe_positive_records_output_file))
    merge_files(maybe_positive_files, maybe_positive_records_output_file)
    logging.info('Merging {} maybe negative labeled files into: {}...'.format(len(maybe_negative_files), maybe_negative_records_output_file))
    merge_files(maybe_negative_files, maybe_negative_records_output_file)
    logging.info('Merging {} process log files into: {}...'.format(len(process_log_files), process_log_file))
    merge_files(process_log_files, process_log_file)

    return (positive_records_output_file, negative_records_output_file, maybe_positive_records_output_file, maybe_negative_records_output_file, process_log_file)

def merge_files(source_files, destination_file_path):
    sharedlib.merge_files(source_files, destination_file_path)

def extract_records(input_files, output_dir, max = None):    
    logging.info('Extracting potential positive and negative records from {} file(s)...'.format(len(input_files)))

    output_dir = sharedlib.abspath(output_dir)

    sharedlib.dump_list_to_file(config.known_positive_records_qualifying_terms, os.path.join(output_dir,  'positive_qualifying_criteria.txt'))
    sharedlib.dump_list_to_file(config.known_positive_records_disqualifying_terms, os.path.join(output_dir,  'positive_disqualifying_criteria.txt'))
    
    total_positive_count = 0
    total_negative_count = 0

    max_records_per_file = config.file_split_lines_per_file

    known_positive_records_qualifying_terms_regex_list = build_compiled_regex_list(config.known_positive_records_qualifying_terms)
    known_positive_records_disqualifying_terms_regex_list = build_compiled_regex_list(config.known_positive_records_disqualifying_terms)
    potential_positive_records_qualifying_terms_regex_list = build_compiled_regex_list(config.potential_positive_records_qualifying_terms)

    for file_name in input_files:
        positive_records_output_files = []
        negative_records_output_files = []
        maybe_positive_records_output_files = []
        maybe_negative_records_output_files = []
        process_log_files = []

        # Split each file for parallelization
        chunks = split_file(file_name, config.file_split_dir, max_records_per_file)
        chunk_max = math.ceil(round(max/len(chunks), 0))
        if chunk_max <= 0:
            chunk_max = 0

        processes = []
        process_return_values = []

        is_first_chunk = True
        for chunk in chunks:
            logging.info('Extracting up to {} potential positive and negative records from {}...'.format(chunk_max, chunk))
            chunk_name_without_ext = os.path.splitext(os.path.basename(chunk))[0]
            positive_records_output_file = os.path.join(output_dir,  chunk_name_without_ext + '.potential_pos.txt')
            negative_records_output_file = os.path.join(output_dir,  chunk_name_without_ext + '.potential_neg.txt')
            maybe_positive_records_output_file = os.path.join(output_dir,  chunk_name_without_ext + '.questionable_pos.txt')
            maybe_negative_records_output_file = os.path.join(output_dir,  chunk_name_without_ext + '.questionable_neg.txt')
            process_log_file =  os.path.join(output_dir,  chunk_name_without_ext + '.process.txt')

            positive_records_output_files.append(positive_records_output_file)
            negative_records_output_files.append(negative_records_output_file)
            maybe_positive_records_output_files.append(maybe_positive_records_output_file)
            maybe_negative_records_output_files.append(maybe_negative_records_output_file)
            process_log_files.append(process_log_file)

            args = (chunk,
                    positive_records_output_file, 
                    negative_records_output_file, 
                    maybe_positive_records_output_file,
                    maybe_negative_records_output_file,
                    process_log_file, 
                    is_positive, 
                    is_negative,
                    known_positive_records_qualifying_terms_regex_list,
                    known_positive_records_disqualifying_terms_regex_list,
                    potential_positive_records_qualifying_terms_regex_list,
                    process_return_values,
                    is_first_chunk, 
                    chunk_max, )

            process = multiprocessing.Process(name=chunk_name_without_ext, target=extract_matching_records_from_file, args=args)
            processes.append(process)

            is_first_chunk = False

        for process in processes:
            logging.info('Starting process: {}...'.format(process.name))
            process.start()

        for process in processes:
            process.join()

        for (positive_count, negative_count) in process_return_values:
            total_positive_count += positive_count
            total_negative_count += negative_count

        # Merge output files
        (positive_records_output_file,
        negative_records_output_file,
        maybe_positive_records_output_file,
        maybe_negative_records_output_file,
        process_log_file) = merge_file_sets(os.path.basename(file_name), output_dir, positive_records_output_files, negative_records_output_files, maybe_positive_records_output_files, maybe_negative_records_output_files, process_log_files)

        logging.info('Deleting temprary chunked files..');
        for chunk in chunks:
            logging.info('Deleting {}...'.format(chunk))
            os.remove(chunk)

        # Upload merged files
        if config.upload_output_to_remote_server == True:
            list_of_files_to_upload = [positive_records_output_file,
                                        negative_records_output_file,
                                        maybe_positive_records_output_file,
                                        maybe_negative_records_output_file,
                                        process_log_file]

            archive_path =  os.path.join(os.path.dirname(positive_records_output_file), os.path.splitext(os.path.basename(file_name))[0]+'.zip')
            sharedlib.zip_files(list_of_files_to_upload, archive_path)
            sharedlib.upload_files_to_labeling_candidates_dir([archive_path])


def extract_matching_records_from_file(input_file, 
                                       positive_records_output_file, 
                                       negative_records_output_file, 
                                       maybe_positive_records_output_file,
                                       maybe_negative_records_output_file,
                                       process_log_file, 
                                       positive_predicate,
                                       negative_predicate,
                                       known_positive_records_qualifying_terms_regexes,
                                       known_positive_records_disqualifying_terms_regexes,
                                       potential_positive_records_qualifying_terms_regexes,
                                       return_values_array,
                                       skip_first_line=True,
                                       max=None
                                       ):
    logging.info('Extracting {} known positive and negative records from file: {}...'.format('ALL' if max == None else max, input_file))

    if not os.path.isabs(input_file):
        input_file = os.path.join(os.path.dirname(__file__), input_file)

    logging.info('Positive records output path: {}...'.format(positive_records_output_file))
    logging.info('Negative records output path: {}...'.format(negative_records_output_file))
    logging.info('Process log path: {}...'.format(process_log_file))

    temp_positive_records_output_file = positive_records_output_file + '.tmp'
    temp_negative_records_output_file = negative_records_output_file + '.tmp'

    file_name = os.path.basename(input_file)
    total_lines = 0
    total_data_lines = 0
    total_positive_data_lines = 0
    total_negative_data_lines = 0
    positive_out_file = open(temp_positive_records_output_file, 'w', encoding='utf-8', errors='ignore')
    maybe_positive_out_file = open(maybe_positive_records_output_file, 'w', encoding='utf-8', errors='ignore')
    negative_out_file = open(temp_negative_records_output_file, 'w', encoding='utf-8', errors='ignore')
    maybe_negative_out_file = open(maybe_negative_records_output_file, 'w', encoding='utf-8', errors='ignore')
    qualification_process_log_file_handle = open(process_log_file, 'w', encoding='utf-8', errors='ignore')
    start_time = datetime.datetime.now()
    process_log_first_line = 'MAUDE Labeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    qualification_process_log_file_handle.write(process_log_first_line)
    fin = codecs.open(input_file, encoding='utf-8', errors='ignore')
    for line in fin:
        sys.stdout.write("{} => POS: {} NEG: {}. Now looking at record: {}... \r".format(file_name, total_positive_data_lines, total_negative_data_lines, total_data_lines))
        sys.stdout.flush()
        total_lines += 1
        if total_lines == 1 and skip_first_line:
            continue
        if max is not None and total_positive_data_lines >= max and total_negative_data_lines >= max:
            break;

        total_data_lines += 1

        if (max is None or total_positive_data_lines < max) and positive_predicate(line, known_positive_records_qualifying_terms_regexes, known_positive_records_disqualifying_terms_regexes, maybe_positive_out_file, qualification_process_log_file_handle):
            positive_out_file.write(line.rstrip() + '\n')
            total_positive_data_lines += 1
            pass
        elif (max is None or total_negative_data_lines < max) and negative_predicate(line, potential_positive_records_qualifying_terms_regexes, maybe_negative_out_file, qualification_process_log_file_handle):
            negative_out_file.write(line.rstrip() + '\n')
            total_negative_data_lines += 1
            pass

        if config.verbose == True or total_lines % 10000 == 0:
            positive_percent = round(total_positive_data_lines / total_data_lines * 100, 2)
            negative_percent = round(total_negative_data_lines / total_data_lines * 100, 2)
            logging.info('{}=>, {} ({}%) positive and {} ({}%) negative records in total {} records so far...'.format(file_name, total_positive_data_lines, positive_percent, total_negative_data_lines, negative_percent, total_data_lines))

    positive_percent = round(total_positive_data_lines / total_data_lines * 100, 2)
    negative_percent = round(total_negative_data_lines / total_data_lines * 100, 2)
    message = '{}=>, {} ({}%) positive and {} ({}%) negative records in the {} records examined in this file'.format(file_name, total_positive_data_lines, positive_percent, total_negative_data_lines, negative_percent, total_data_lines)
    logging.info(message)
    qualification_process_log_file_handle.write(message + '\n')
    fin.close()
    positive_out_file.close()
    maybe_positive_out_file.close()
    negative_out_file.close()
    maybe_negative_out_file.close()

    if config.match_extracted_positive_negative_records_count and total_positive_data_lines != total_negative_data_lines:
        if total_positive_data_lines < total_negative_data_lines:
            extract_random_records(temp_negative_records_output_file, negative_records_output_file, total_positive_data_lines, 1, total_negative_data_lines, qualification_process_log_file_handle)
            shutil.move(temp_positive_records_output_file, positive_records_output_file)
            os.remove(temp_negative_records_output_file)
        elif total_negative_data_lines < total_positive_data_lines:
            extract_random_records(temp_positive_records_output_file, positive_records_output_file, total_negative_data_lines, 1, total_positive_data_lines, qualification_process_log_file_handle)
            shutil.move(temp_negative_records_output_file, negative_records_output_file)
            os.remove(temp_positive_records_output_file)
    else:
            shutil.move(temp_positive_records_output_file, positive_records_output_file)
            shutil.move(temp_negative_records_output_file, negative_records_output_file)

    end_time = datetime.datetime.now()
    qualification_process_log_file_handle.write('Labeling completed at {}. Duration: {} \n'.format(end_time, end_time - start_time))
    qualification_process_log_file_handle.close()

    return_values_array.append((total_positive_data_lines, total_negative_data_lines))

def extract_random_records(input_file_path, output_file_path, number_of_records_to_extract, min_record_index, max_record_index, log_file_handle):
    msg = 'Extracting random {} records from {} into {}\n'.format(number_of_records_to_extract, input_file_path, output_file_path)
    log_file_handle.write(msg) 
    logging.info(msg)

    lines_to_extract = random.sample(range(min_record_index, max_record_index), number_of_records_to_extract)

    line_number = 0
    with open(output_file_path, 'w',  encoding='utf-8', errors='ignore') as fout:
        with open(input_file_path, 'r',  encoding='utf-8', errors='ignore') as fin:
            for line in fin:
                line_number += 1
                if line_number in lines_to_extract:
                    fout.write(line)

def build_compiled_regex_list(list_of_patterns):
    return [re.compile(p, re.IGNORECASE) for p in list_of_patterns]

def is_positive(line, known_positive_records_qualifying_terms_regexes, known_positive_records_disqualifying_terms_regexes, questionable_records_file, qualification_process_log_file_handle):
    likely_positive = False
    for pattern in known_positive_records_qualifying_terms_regexes:
        match = re.search(pattern, line)
        if match is not None:
            likely_positive = True
            qualification_process_log_file_handle.write(line[:50] + '... POSITIVE MATCHED ON: ' + match.group() + '\n')
            break

    if likely_positive == False:
        return False

    for pattern in known_positive_records_disqualifying_terms_regexes:
        match = re.search(pattern, line)
        if match is not None:
            questionable_records_file.write(line)
            qualification_process_log_file_handle.write(line[:50] + '... POSITIVE MATCHED BUT DISQUALIFIED DUE TO  MATCH ON: ' + match.group() + '\n')
            return False

    return True

def is_negative(line, potential_positive_records_qualifying_terms_regexes, questionable_records_file, qualification_process_log_file_handle):
    for pattern in potential_positive_records_qualifying_terms_regexes:
        match = re.search(pattern, line)
        if match is not None: # No match found on any potential signals
            questionable_records_file.write(line)
            qualification_process_log_file_handle.write(line[:50] + '... LIKELY NEGATIVE BUT DISQUALIFIED DUE TO MATCH ON: ' + match.group() + '\n')
            return False

    return True