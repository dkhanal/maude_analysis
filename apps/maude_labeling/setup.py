# By Deepak Khanal
# dkhanal@gmail.com

import sys
import os

def create_dirs():
    base_path = os.path.dirname(__file__)

    out_dir = os.path.join(base_path, 'out')

    if not os.path.exists(out_dir):
        print('Creating directory: {}'.format(out_dir))
        os.makedirs(out_dir)

def add_lib_to_path():
    base_path = os.path.dirname(__file__)
    lib = os.path.join(base_path, 'lib')

    if lib not in sys.path:
        print('Adding to sys.path: {}'.format(lib))
        sys.path.append(lib)
    else:
        print('Already in sys.path: {}'.format(lib))

# Setup process:
create_dirs()
add_lib_to_path()
