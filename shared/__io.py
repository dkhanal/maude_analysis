# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import shutil
import string
import re
import hashlib
import logging
import random

def initialize(current_app_path):
    global __current_app_path
    __current_app_path = os.path.dirname(current_app_path)

def create_dirs(list_of_paths):
    for path in list_of_paths:
        path = os.path.abspath(path)
        logging.info('Creating directory: {}'.format(path))
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            logging.info('Directory: {} already exists.'.format(path))

def abspath(path):
    if not os.path.isabs(path):
        path = os.path.abspath(os.path.join(os.path.dirname(__current_app_path), path))
    return path


def copy_files(files_to_copy, destn_dir, skip_if_existing = False):
    for file in files_to_copy:
        dstn_path = os.path.join(destn_dir, os.path.basename(file))
        copy_file(file, dstn_path)

def copy_file(src_file, destn_file, skip_if_existing = False):
    logging.info('Copying {} as {}...'.format(src_file, destn_file))            
    destn_dir = os.path.dirname(destn_file)
    if not os.path.exists(destn_dir):
        logging.info('Directory {} does not exist. Creating new...'.format(destn_dir))            
        os.makedirs(destn_dir)

    if os.path.exists(destn_file):
        if skip_if_existing == True:
            logging.info('Skipping copy. File already exists: {}.'.format(destn_file))            
            return

        logging.info('File already exists. Deleting: {}.'.format(destn_file))            
        os.remove(destn_file)
                         
    shutil.copyfile(src_file, destn_file)

def merge_files(source_files, destination_file_path, skip_duplicates = False, duplicate_record_check_ignore_pattern = None):        
    line_hash_dict = {}
    dup_check_ignore_pattern_regex = re.compile(duplicate_record_check_ignore_pattern) if duplicate_record_check_ignore_pattern is not None else None
    with open(destination_file_path, 'w',  encoding='utf-8', errors='ignore') as fout:
        for file_chunk in source_files:
            logging.info('Merging {} into {}...'.format(os.path.basename(file_chunk), destination_file_path))
            with open(file_chunk, 'r',  encoding='utf-8', errors='ignore') as fin:
                line_number = 0
                for line in fin:
                    line_number += 1
                    sys.stdout.write("Merging record {}... \r".format(line_number))
                    sys.stdout.flush()

                    if skip_duplicates == True:

                        line_to_hash = None
                        if dup_check_ignore_pattern_regex is not None:
                            line_to_hash = re.sub(dup_check_ignore_pattern_regex, '', line)
                        else:
                            line_to_hash = line
                        
                        line_hash = hashlib.sha1(line_to_hash.upper().encode(errors='ignore')).hexdigest()
                        line_id = line[:40]

                        if line_hash in line_hash_dict:
                            logging.info('DUPLICATE - Record {} is a duplicate of {}. It will be ignored'.format(line_id, line_hash_dict[
                                line_hash]))
                            continue
                        line_hash_dict[line_hash] = line_id                
                        
                    fout.write(line)

def randomize_records(file_path):
    # Randomizes records in the specified file. Current implementation is memory-bound 
    # and very not suitable for files containing more than 10,000 records.
    logging.info('Randomizing (in place) records in {}...'.format(file_path))
    records = None
    with open(file_path, 'r',  encoding='utf-8', errors='ignore') as fin:
        records = [record for record in fin]
    random.shuffle(records)
    written_record_count = 0
    with open(file_path, 'w',  encoding='utf-8', errors='ignore') as fout:
        for record in records:
            fout.write(record)
            written_record_count += 1
    logging.info('Randomized all {} of {} records in {}...'.format(written_record_count, len(records), file_path))


def remove_duplicate_records(files_to_read_and_update):
    # Performs in place removal of duplicate records across files. 
    # In case of duplicates across multiple files, the file where the record is first found wins.

    logging.info('Removing duplicates across {} files...'.format(len(files_to_read_and_update)))
    record_hash_dict = {}
    for file in files_to_read_and_update: 
        file_name = os.path.basename(file)
        unique_records = []
        read_record_count = 0
        with open(file, 'r',  encoding='utf-8', errors='ignore') as fin:
            for line in fin:
                read_record_count += 1
                record_hash = hashlib.sha1(line.upper().encode(errors='ignore')).hexdigest()
                record_id = "{}=>{}".format(file_name, line[:40])

                if record_hash in record_hash_dict:
                    logging.info('DUPLICATE - Record {} is a duplicate of {}. It will be removed.'.format(record_id, record_hash_dict[record_hash]))
                    continue

                record_hash_dict[record_hash] = record_id                
                unique_records.append(line)

        written_record_count = 0
        with open(file, 'w',  encoding='utf-8', errors='ignore') as fout:
            for line in unique_records:
                fout.write(line)
                written_record_count += 1

        logging.info('Eliminated {} duplicate records from {}. Read: {}, Written: {}'.format(read_record_count - written_record_count, file_name, read_record_count, written_record_count))

def read_all_records(file_path):
    logging.info('Reading all records into list from {}...'.format(file_path))
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fin:
        return [line for line in fin]

def save_list_to_file(list, file_path):
    logging.info('Writing all {} records from list to {}...'.format(len(list), file_path))
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as fout:
        for line in list:
            fout.write(line)

def get_total_lines_count(file_path):
    line_count = 0
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_count += 1

    print('Total {} lines in {}'.format(line_count, file_path))
    return line_count


# The inline code is to register get_char_input() in a platform-agnostic way.
# The code below executes when this module is loaded.
try:
    import tty, termios
except ImportError:
    try:
        import msvcrt
    except ImportError:
        raise ImportError('Unrecognized Computing Environment!')
    else:
        get_char_input = msvcrt.getch
else:
    def get_char_input():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


