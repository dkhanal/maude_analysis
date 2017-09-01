# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import __logging
import __env
import __io
import __remote_server
import __http
import __zip
import __pickle
import __collections

# Initialization
def initialize(application_abs_path, log_file_abs_path, remote_server_base_uri):
    __io.initialize(application_abs_path)
    __logging.initialize(log_file_abs_path)
    __remote_server.initialize(remote_server_base_uri)

# Logging related
def close_logger():
    __logging.close_logger()

# Environemnt variables
def load_environment_vars(setenv_path):
    __env.load_environment_vars(setenv_path)

# I/O
def create_dirs(list_of_paths):
    __io.create_dirs(list_of_paths)

def abspath(path):
    return __io.abspath(path)

def get_char_input():
    return __io.get_char_input()

# Cloud
def upload_files_to_remote_server(list_of_files, remote_directory):
    __remote_server.upload_files_to_remote_server(list_of_files, remote_directory)

def get_list_of_files_from_remote_server(remote_directory):
    return __remote_server.get_list_of_files_from_remote_server(remote_directory)

# HTTP
def download_file(url, save_to_path, force_download=False):
    return __http.download_file(url, save_to_path, force_download)

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