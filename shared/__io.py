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


