# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import logging

def load_environment_vars(setenv_path):
    logging.info('Loading application environment variables...')
    if os.path.isfile(setenv_path):
        script = open(setenv_path)
        exec(script.read())
    else:
        logging.warning('No environment variables set ({} not found). Configuration may be incomplete.'.format(setenv_path))
