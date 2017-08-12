# By Deepak Khanal
# dkhanal@gmail.com

import sys
import os
import shutil
import stat

def create_dirs():
    base_path = os.path.abspath(os.path.dirname(__file__))

    out_dir = os.path.join(base_path, 'out')
    models_dir = os.path.join(base_path, 'models')

    initialize_dir(out_dir)
    initialize_dir(models_dir)

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

def initialize_dir(path):
    print('Initializing {}...'.format(path))
    if os.path.exists(path):
        for file in os.listdir(path):
            print('Deleting {}...'.format(file))
            os.remove(os.path.join(path, file))
    
        shutil.rmtree(path, onerror=on_rmtree_error)

    if not os.path.exists(path):
        print('Creating directory: {}'.format(path))
        os.makedirs(path)


def on_rmtree_error(operation, path, exception):
    print('Could not remove {}. Error (ignored): {}'.format(path, exception))

# Setup process:
create_dirs()
add_lib_to_path()
set_environment_vars()
