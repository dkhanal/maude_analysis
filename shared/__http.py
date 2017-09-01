# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import urllib
import logging

def download_file(url, save_to_path, force_download=False):
    logging.info('Downloading {} to {}. This may take a while...'.format(url, save_to_path))
    if force_download == False and os.path.exists(save_to_path):
        logging.info('File {} already exists. It will not be downloaded.'.format(save_to_path))
        return
    urllib.request.urlretrieve(url, save_to_path)
