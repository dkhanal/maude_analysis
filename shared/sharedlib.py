# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import __logging
import __env
import __io
import __azure
import __http
import __zip
import __pickle
import __collections

# Logging related
def initialize_logger(log_file_abs_path):
    __logging.initialize_logger(log_file_abs_path)

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

def set_current_app_path(path):
    __io.set_current_app_path(path)

# Cloud
def upload_files_to_cloud_container(list_of_files, container_name):
    __azure.upload_files_to_container(list_of_files, container_name)

def get_list_of_files_in_cloud_container(container_name):
    return __azure.get_list_of_files_in_container(container_name)

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