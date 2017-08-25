# By Deepak Khanal
# dkhanal@gmail.com

import sys
import os
import shutil
import stat

def create_dirs():
    base_path = os.path.abspath(os.path.dirname(__file__))

    in_dir = os.path.join(base_path, 'in')
    out_dir = os.path.join(base_path, 'out')

    if not os.path.exists(in_dir):
        print('Creating directory: {}'.format(in_dir))
        os.makedirs(in_dir)

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

def set_environment_vars():
    env_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.setenv.py'))
    if os.path.isfile(env_script_path):
        script = open(env_script_path)
        exec(script.read())
    else:
        print ('WARN: No environment variables set (.setenv.py not found). Configuration may be incomplete.')

# Setup process:
create_dirs()
add_lib_to_path()
set_environment_vars()
