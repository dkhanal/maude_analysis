import os
import datetime
import urllib
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

import util
import config

def all_work_in_progress_files_present_on_cloud(cloud_files):
    print('Checking for the presence of cloud files...')
    print('Connecting to Azure Blob Storage. Container: {}'.format(cloud_files['container']))
    block_blob_service = BlockBlobService(config.azure_account_name, config.azure_account_key)

    blobs = [item.name for item in block_blob_service.list_blobs(cloud_files['container'])]
    if not cloud_files['potential_positive_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['potential_positive_records_blob']))
        return False

    if not cloud_files['potential_negative_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['potential_negative_records_blob']))
        return False

    if not cloud_files['questionable_positive_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['questionable_positive_records_blob']))
        return False

    if not cloud_files['questionable_negative_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['questionable_negative_records_blob']))
        return False

    if not cloud_files['verified_positive_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['verified_positive_records_blob']))
        return False

    if not cloud_files['verified_negative_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['verified_negative_records_blob']))
        return False

    if not cloud_files['already_processed_record_numbers_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['already_processed_record_numbers_blob']))
        return False

    return True

def download_file(url, destination_path, force_download=False):
    file_path = util.fix_path(destination_path)
    if force_download == False and config.cloud_files['skip_input_files_download_if_already_present'] == True and os.path.exists(file_path):
        print('File {} already exists. It will not be downloaded.'.format(file_path))
        return

    print('Downloading {} to {}. This may take a while...'.format(url, file_path))
    urllib.request.urlretrieve(url, file_path)

def download_cloud_files(cloud_files, output_files):
    base_url = cloud_files['base_url']
    print('Downloading cloud files from {}'.format(base_url))
    
    download_file(base_url + cloud_files['potential_positive_records_blob'], output_files['potential_positive_records_file'])
    download_file(base_url + cloud_files['potential_negative_records_blob'], output_files['potential_negative_records_file'])
    download_file(base_url + cloud_files['questionable_positive_records_blob'], output_files['questionable_positive_records_file'])    
    download_file(base_url + cloud_files['questionable_negative_records_blob'], output_files['questionable_negative_records_file'])

    download_file(base_url + cloud_files['verified_positive_records_blob'], output_files['verified_positive_records_file'], True)
    download_file(base_url + cloud_files['verified_negative_records_blob'], output_files['verified_negative_records_file'], True)
    download_file(base_url + cloud_files['already_processed_record_numbers_blob'], output_files['already_processed_record_numbers_file'], True)

def upload_files(list_of_files, container_name):
    start_time = datetime.datetime.now()
    print('Uploading {} files to cloud. Starting at {}'.format(len(list_of_files), start_time))
    
    print('Connecting to Azure Blob Storage...')

    block_blob_service = BlockBlobService(config.azure_account_name, config.azure_account_key)

    for file in list_of_files:
        file_abs = util.fix_path(file)
        file_basename = os.path.basename(file_abs)
        print('Uploading {} to the Cloud...'.format(file))
        block_blob_service.create_blob_from_path(container_name, 
                                                 file_basename, file_abs,
                                                 content_settings=ContentSettings(content_type='text/plain'))

    end_time = datetime.datetime.now()
    print('Upload completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
