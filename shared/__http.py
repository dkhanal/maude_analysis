# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import urllib
import logging

def download_file(url, save_to_path):
    urllib.request.urlretrieve(url, save_to_path)
