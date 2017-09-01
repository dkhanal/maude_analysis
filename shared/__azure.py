# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import datetime
import logging

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

def __load_credentials():
    azure_account_name = os.environ['azure_account_name']
    azure_account_key = os.environ['azure_account_key']

    if len(azure_account_key.strip()) == 0 or len(azure_account_key.strip())  == 0:
        logging.error('Cannot upload files to cloud. Cloud credentials are not set.')
        raise ValueError('Azure credentials have not been set. Cannot connect to Azure.')

    return (azure_account_name, azure_account_key)

def upload_files_to_directory(list_of_files, directory_name):
    logging.info('Connecting to Azure Blob Storage...')
    azure_account_name, azure_account_key = __load_credentials()
    block_blob_service = BlockBlobService(azure_account_name, azure_account_key)

    for file in list_of_files:
        file_basename = os.path.basename(file)
        logging.info('Uploading {} to the Remote Server...'.format(file))
        block_blob_service.create_blob_from_path(directory_name,
                                                 file_basename, file,
                                                 content_settings=ContentSettings(content_type=__get_mime_type(file_basename)))

def get_list_of_files_in_directory(directory_name):
    logging.info('Getting a list of files from directory: {}..'.format(directory_name))
    logging.info('Connecting to Azure Blob Storage...')

    azure_account_name, azure_account_key = __load_credentials()
    block_blob_service = BlockBlobService(azure_account_name, azure_account_key)

    blobs = [item.name for item in block_blob_service.list_blobs(directory_name)]

    return blobs



def __get_mime_type(filename):
    filename_lower = filename.lower()
    if '.zip' in filename_lower:
        return 'application/zip'
    else:
        return 'text/plain'