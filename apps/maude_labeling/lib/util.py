# By Deepak Khanal
# dkhanal@gmail.com

import os
import pickle
import zipfile
import sys

def fix_path(p):
    if not os.path.isabs(p):
        p = os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    return p

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

def unzip(zip_file_path, target_dir):
    compressed = zipfile.ZipFile(zip_file_path, 'r')
    compressed.extractall(target_dir)
    compressed.close()
