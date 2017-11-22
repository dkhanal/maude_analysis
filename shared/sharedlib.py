# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os

import __logging
import __env
import __io
import __remote_server
import __http
import __zip
import __pickle
import __collections
import __exception

# Initialization
def initialize(application_abs_path, log_file_abs_path, remote_server_config):
    global app_dir
    app_dir = os.path.dirname(application_abs_path)

    __io.initialize(app_dir)
    __logging.initialize(log_file_abs_path)
    __exception.initialize()
    __remote_server.initialize(remote_server_config)
    __env.load_environment_vars(os.path.join(app_dir, '.setenv.py'))

# Logging related
def close_logger():
    __logging.close_logger()

# Environment variables
def reload_environment_vars(setenv_path):
    __env.load_environment_vars(setenv_path)

# I/O
def create_dirs(list_of_paths):
    __io.create_dirs(list_of_paths)

def abspath(path):
    return __io.abspath(path)

def get_char_input():
    return __io.get_char_input()

def merge_files(source_files, destination_file_path, skip_duplicates = False, duplicate_record_check_ignore_pattern = None):
    __io.merge_files(source_files, destination_file_path, skip_duplicates, duplicate_record_check_ignore_pattern)

def randomize_records(file_path):
    __io.randomize_records(file_path)

def remove_duplicate_records(files_to_read_and_update):
    # Performs in place removal of duplicate records across files. 
    # In case of duplicates across multiple files, the file where the record is first found wins.
    __io.remove_duplicate_records(files_to_read_and_update)

def read_all_records(file_path):
    return __io.read_all_records(file_path)

def save_list_to_file(list, file_path):
    __io.save_list_to_file(list, file_path)

def get_total_lines_count(file_path):
    return __io.get_total_lines_count(file_path)

# Cloud
def join_remote_server_paths(path1, path2, path3=None):
    return __remote_server.join_remote_server_paths(path1, path2, path3)

def upload_files_to_remote_server(list_of_files, remote_directory):
    __remote_server.upload_files_to_remote_server(list_of_files, remote_directory)

def upload_files_to_remote_server_with_prompt(list_of_files, remote_directory):
    __remote_server.upload_files_to_remote_server_with_prompt(list_of_files, remote_directory)

def get_list_of_files_from_remote_server(remote_directory):
    return __remote_server.get_list_of_files_from_remote_server(remote_directory)

def upload_files_to_labeling_candidates_dir(list_of_files):
    __remote_server.upload_files_to_labeling_candidates_dir(list_of_files)

def upload_files_to_labeling_auto_labeled_dir(list_of_files):
    __remote_server.upload_files_to_labeling_auto_labeled_dir(list_of_files)

def upload_files_to_labeling_verified_samples_dir(list_of_files):
    __remote_server.upload_files_to_labeling_verified_samples_dir(list_of_files)

def upload_files_to_trained_models_dir(list_of_files):
    __remote_server.upload_files_to_trained_models_dir(list_of_files)

def upload_files_to_classified_dir(list_of_files):
    __remote_server.upload_files_to_classified_dir(list_of_files)

def download_file(url, save_to_path, force_download=False):
    __remote_server.download_file(url, save_to_path, force_download)


# Zip
def zip_files(list_of_files, zip_file_path):
    return __zip.zip_files(list_of_files, zip_file_path)

def unzip(zip_file_path, output_dir_path):
    __zip.unzip(zip_file_path, output_dir_path)

# Pickle
def pickle_object(obj, pickle_file_path):
    __pickle.pickle_object(obj, pickle_file_path)

def load_pickle(pickle_file_path):
    return __pickle.load_pickle(pickle_file_path)

# Collections
def dump_list_to_file(list_to_dump, output_dump_file):
    __collections.dump_list_to_file(list_to_dump, output_dump_file)