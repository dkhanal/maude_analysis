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
    print(blobs)
    if not cloud_files['potential_positive_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['potential_positive_records_blob']))
        return False

    if not cloud_files['potential_negative_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['potential_negative_records_blob']))
        return False

    if not cloud_files['verified_positive_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['verified_positive_records_blob']))
        return False

    if not cloud_files['verified_negative_records_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['verified_negative_records_blob']))
        return False

    if not cloud_files['last_processed_record_number_blob'] in blobs:
        print('Could not find file {} on the Cloud'.format(cloud_files['last_processed_record_number_blob']))
        return False

    return True

def download_file(url, destination_path):
    file_path = util.fix_path(destination_path)
    print('Downloading {} to {}. This may take a while...'.format(url, file_path))
    urllib.request.urlretrieve(url, file_path)

def download_cloud_files(cloud_files, output_files):
    base_url = cloud_files['base_url']
    download_file(base_url + cloud_files['potential_positive_records_blob'], output_files['potential_positive_records_file'])
    download_file(base_url + cloud_files['potential_negative_records_blob'], output_files['potential_negative_records_file'])
    download_file(base_url + cloud_files['verified_positive_records_blob'], output_files['verified_positive_records_file'])
    download_file(base_url + cloud_files['verified_negative_records_blob'], output_files['verified_negative_records_file'])
    download_file(base_url + cloud_files['last_processed_record_number_blob'], output_files['last_processed_record_number_file'])

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
