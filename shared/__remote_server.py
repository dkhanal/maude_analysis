# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import datetime
import urllib
import os
import shutil
import logging

import __io
import __azure
import __http

__CLOUD = 'cloud'
__FILESYSTEM = 'filesystem'



def initialize(remote_server_config):
    global __remote_server_config
    global __remote_server_type

    global __base_uri

    global __narratives_dir
    global __labeling_candidates_dir
    global __labeling_auto_labeled_dir
    global __labeling_verified_samples_dir
    global __trained_models_dir
    global __classified_dir


    global __narratives_uri
    global __labeling_candidates_uri
    global __autolabeled_uri
    global __labeled_uri
    global __models_uri
    global __classification_uri

    if remote_server_config is None:
        raise ValueError('remote_server_config not specified.')

    if not 'base_uri' in remote_server_config:
        raise ValueError('base_uri not specified in remote server config.')

    if not 'narratives_dir' in remote_server_config:
        raise ValueError('narratives_dir not specified in remote server config.')

    if not 'labeling_candidates_dir' in remote_server_config:
        raise ValueError('labeling_candidates_dir not specified in remote server config.')

    if not 'labeling_verified_samples_dir' in remote_server_config:
        raise ValueError('labeling_verified_samples_dir not specified in remote server config.')

    if not 'trained_models_dir' in remote_server_config:
        raise ValueError('trained_models_dir not specified in remote server config.')

    if not 'classified_dir' in remote_server_config:
        raise ValueError('classified_dir not specified in remote server config.')

    __remote_server_config = remote_server_config

    __base_uri = remote_server_config['base_uri']
    __narratives_dir = remote_server_config['narratives_dir']
    __labeling_candidates_dir = remote_server_config['labeling_candidates_dir']
    __labeling_auto_labeled_dir = remote_server_config['labeling_auto_labeled_dir']
    __labeling_verified_samples_dir = remote_server_config['labeling_verified_samples_dir']
    __trained_models_dir = remote_server_config['trained_models_dir']
    __classified_dir = remote_server_config['classified_dir']

    base_uri = __remote_server_config['base_uri']
    base_uri_lower = base_uri.lower()
    if 'http://' in base_uri_lower or 'https://' in base_uri_lower:
        __remote_server_type = __CLOUD
    else:
        __remote_server_type = __FILESYSTEM


    if __remote_server_type == __CLOUD:
        __narratives_uri = urllib.parse.urljoin(base_uri, __narratives_dir)
        __labeling_candidates_uri = urllib.parse.urljoin(base_uri, __labeling_candidates_dir)
        __autolabeled_uri = urllib.parse.urljoin(base_uri, __labeling_auto_labeled_dir)
        __labeled_uri = urllib.parse.urljoin(base_uri, __labeling_verified_samples_dir)
        __models_uri = urllib.parse.urljoin(base_uri, __trained_models_dir)
        __classification_uri = urllib.parse.urljoin(base_uri, __classified_dir)
    else:
        __narratives_uri = os.path.join(base_uri, __narratives_dir)
        __labeling_candidates_uri = os.path.join(base_uri, __labeling_candidates_dir)
        __autolabeled_uri = os.path.join(base_uri, __labeling_auto_labeled_dir)
        __labeled_uri = os.path.join(base_uri, __labeling_verified_samples_dir)
        __models_uri = os.path.join(base_uri, __trained_models_dir)
        __classification_uri = os.path.join(base_uri, __classified_dir)


def upload_files_to_labeling_candidates_dir(list_of_files):
    upload_files_to_remote_server(list_of_files, __labeling_candidates_dir)

def upload_files_to_labeling_auto_labeled_dir(list_of_files):
    upload_files_to_remote_server(list_of_files, __labeling_auto_labeled_dir)

def upload_files_to_labeling_verified_samples_dir(list_of_files):
    upload_files_to_remote_server(list_of_files, __labeling_verified_samples_dir)

def upload_files_to_trained_models_dir(list_of_files):
    upload_files_to_remote_server(list_of_files, __trained_models_dir)

def upload_files_to_classified_dir(list_of_files):
    upload_files_to_remote_server(list_of_files, __classified_dir)


def upload_files_to_remote_server(list_of_files, remote_directory):
    if list_of_files is None:
        return
    
    start_time = datetime.datetime.now()
    logging.info('Uploading {} files to directory {} in the Remote Server. Starting at {}...'.format(len(list_of_files), remote_directory, start_time))
    if __remote_server_type == __CLOUD:
        __azure.upload_files_to_directory(list_of_files, remote_directory)
    elif __remote_server_type == __FILESYSTEM:
        __io.copy_files(list_of_files,  os.path.join(__base_uri, remote_directory))
    else:
        logging.error('Remote Server of type {}  is not supported'.format(__remote_server_type))

    end_time = datetime.datetime.now()
    logging.info('Upload completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


def get_list_of_files_from_remote_server(remote_directory):
    logging.info('Getting a list of files from directory ({}) in the Remote Server...'.format(remote_directory))

    if __remote_server_type == __CLOUD:
        return __azure.get_list_of_files_from_remote_server(remote_directory)
    elif __remote_server_type == __FILESYSTEM:

        complete_dir = join_remote_server_paths(__base_uri, remote_directory)

        if not os.path.exists(complete_dir):
            return []

        return os.listdir()
    else:
        logging.error('Remote Server of type {}  is not supported'.format(__remote_server_type))

    return None

def download_file(url, save_to_path, force_download=False):
    logging.info('Downloading {} to {}. This may take a while...'.format(url, save_to_path))
    if force_download == False and os.path.exists(save_to_path):
        logging.info('File {} already exists. It will not be downloaded.'.format(save_to_path))
        return

    if __remote_server_type == __CLOUD:
        __http.download_file(url, save_to_path)

    elif __remote_server_type == __FILESYSTEM:
        __io.copy_file(url, save_to_path)

    else:
        logging.error('Remote Server of type {}  is not supported'.format(__remote_server_type))


def join_remote_server_paths(path1, path2, path3=None):
    if __remote_server_type == __CLOUD:
        real_path1 = path1 + '/' if not path1.endswith('/') else path1
        result = urllib.parse.urljoin(real_path1, path2)

        if path3 is not None:
            real_result = result + '/' if not result.endswith('/') else result
            result =   urllib.parse.urljoin(real_result, path3)
            return result
            
        return result
    else:
        if path3 is None:
            return os.path.join(path1, path2)
        return os.path.join(path1, path2, path3)

def upload_files_to_remote_server_with_prompt(list_of_files, remote_directory):
    logging.info(list_of_files)
    logging.info('Upload these {} files to directory ({}) on ({})? [y/n] '.format(len(list_of_files), remote_directory, __base_uri))
    upload_confirmation = __io.get_char_input()
    if not isinstance(upload_confirmation, str):
        upload_confirmation = bytes.decode(upload_confirmation)
    if upload_confirmation == 'y':
        upload_files_to_remote_server(list_of_files, remote_directory)
    else:
        logging.info('Upload canceled on user request.')