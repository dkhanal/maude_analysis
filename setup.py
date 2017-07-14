# By Deepak Khanal
# dkhanal@gmail.com

# To manually execute:
# >> exec(open('C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_sw_causes\\setup.py').read())

import sys
import os
import urllib.request
import multiprocessing

def create_dirs():
    base_path = os.path.dirname(__file__)

    data_dir = os.path.join(base_path, 'data')
    out_dir = os.path.join(base_path, 'out')
    pickles_dir = os.path.join(base_path, 'pickles')

    if not os.path.exists(data_dir):
        print('Creating directory: {}'.format(data_dir))
        os.makedirs(data_dir)

    if not os.path.exists(out_dir):
        print('Creating directory: {}'.format(out_dir))
        os.makedirs(out_dir)

    if not os.path.exists(pickles_dir):
        print('Creating directory: {}'.format(pickles_dir))
        os.makedirs(pickles_dir)

def add_lib_to_path():
    base_path = os.path.dirname(__file__)
    lib = os.path.join(base_path, 'lib')

    if lib not in sys.path:
        print('Adding to sys.path: {}'.format(lib))
        sys.path.append(lib)
    else:
        print('Already in sys.path: {}'.format(lib))

def download_file(args):
    url, destination_path = args

    file_path = os.path.abspath(destination_path)

    if os.path.isfile(file_path):
        print ('Data file {} already exists. It will not be downloaded.'.format(file_path))
        return

    print('Downloading {} to {}. It may take a while.'.format(url, file_path))
    urllib.request.urlretrieve(url, file_path)

def download_data_files():
    base_path = os.path.dirname(__file__)
    data_file_urls = [
        ('https://maude.blob.core.windows.net/narratives/foitext2007.txt', os.path.join(base_path, 'data', 'foitext2007.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2008.txt', os.path.join(base_path, 'data', 'foitext2008.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2009.txt', os.path.join(base_path, 'data', 'foitext2009.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2010.txt', os.path.join(base_path, 'data', 'foitext2010.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2011.txt', os.path.join(base_path, 'data', 'foitext2011.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2012.txt', os.path.join(base_path, 'data', 'foitext2012.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2013.txt', os.path.join(base_path, 'data', 'foitext2013.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2014.txt', os.path.join(base_path, 'data', 'foitext2014.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2015.txt', os.path.join(base_path, 'data', 'foitext2015.txt')),
        ('https://maude.blob.core.windows.net/narratives/foitext2016.txt', os.path.join(base_path, 'data', 'foitext2016.txt')),
        ]

    print('Checking if data files need to be downloaded...')
    for item in data_file_urls:
        download_file(item)

# Setup process:
create_dirs()
add_lib_to_path()
download_data_files()