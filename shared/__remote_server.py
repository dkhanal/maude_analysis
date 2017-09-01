# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import datetime
import logging
import __azure

def initialize(base_uri):
    global __remote_server_base_uri
    global __remote_server_type

    if base_uri is None:
        return

    __remote_server_base_uri = base_uri

    base_uri_lower = base_uri.lower()
    if 'http://' in base_uri_lower or 'https://' in base_uri_lower:
        __remote_server_type = 'cloud'
    else:
        __remote_server_type = 'filesystem'


def upload_files_to_remote_server(list_of_files, remote_directory):
    start_time = datetime.datetime.now()
    logging.info('Uploading {} files to directory {} in the Remote Server. Starting at {}...'.format(len(list_of_files), remote_directory, start_time))
    if __remote_server_type == 'cloud':
        __azure.upload_files_to_directory(list_of_files, remote_directory)
    else:
        logging.error('Remote Server of type {}  is not supported'.format(__remote_server_type))

    end_time = datetime.datetime.now()
    logging.info('Upload completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


def get_list_of_files_from_remote_server(remote_directory):
    logging.info('Getting a list of files from directory {} in the Remote Server...'.format(remote_directory))

    if __remote_server_type == 'cloud':
        return __azure.get_list_of_files_from_remote_server(remote_directory)
    else:
        logging.error('Remote Server of type {}  is not supported'.format(__remote_server_type))

    return None