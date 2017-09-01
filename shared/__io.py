# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import sys
import logging

def set_current_app_path(path):
    global __current_app_path
    __current_app_path = os.path.dirname(path)

def create_dirs(list_of_paths):
    for path in list_of_paths:
        path = os.path.abspath(path)
        logging.info('Creating directory: {}'.format(path))
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            logging.info('Directory: {} already exists.'.format(path))

def abspath(path):
    if not os.path.isabs(path):
        path = os.path.abspath(os.path.join(os.path.dirname(__current_app_path), path))
    return path


# The inline code is to register get_char_input() in a platform-agnostic way.
# The code below executes when this module is loaded.
try:
    import tty, termios
except ImportError:
    try:
        import msvcrt
    except ImportError:
        raise ImportError('Unrecognized Computing Environment!')
    else:
        get_char_input = msvcrt.getch
else:
    def get_char_input():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


