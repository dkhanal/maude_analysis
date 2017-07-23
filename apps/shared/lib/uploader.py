import os
import datetime
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

import util
import config

def upload_files(list_of_files, temp_zip_dir, upload_zip_file_name):
    zip_file_base_name = os.path.basename(upload_zip_file_name)
    start_time = datetime.datetime.now()
    print('Uploading {} files to cloud. Starting at {}'.format(len(list_of_files), start_time))
    
    print('Archiving files into {}'.format(zip_file_base_name))
    zip_file_path = os.path.join(temp_zip_dir, zip_file_base_name)
    util.zip_files(list_of_files, upload_zip_file_name)

    print('Connecting to Azure Blob Storage...')

    block_blob_service = BlockBlobService(config.azure_account_name, config.azure_account_key)

    print('Uploading {} to the Cloud...'.format(upload_zip_file_name))
    block_blob_service.create_blob_from_path(config.cloud_blob_container_name, 
                                             zip_file_base_name, zip_file_path,
                                             content_settings=ContentSettings(content_type='application/zip'))

    end_time = datetime.datetime.now()
    print('Upload completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))
