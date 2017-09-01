# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import zipfile
import logging

def zip_files(list_of_files, zip_file_path):
    logging.info('Zipping files as: {}'.format(zip_file_path))
    compressed_stream = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
    for source_file in list_of_files:
        file_base_name = os.path.basename(source_file)
        logging.info('Compressing {}...'.format(file_base_name))
        compressed_stream.write(source_file, file_base_name)
    compressed_stream.close()
    return zip_file_path

def unzip(zip_file_path, target_dir):
    logging.info('Unzipping {} to {}'.format(zip_file_path, target_dir))
    compressed = zipfile.ZipFile(zip_file_path, 'r')
    compressed.extractall(target_dir)
    compressed.close()