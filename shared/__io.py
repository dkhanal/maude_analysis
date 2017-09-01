# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import shutil
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


