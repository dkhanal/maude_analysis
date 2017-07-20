# By Deepak Khanal
# dkhanal@gmail.com

import os
import pickle

def dump_list_to_file(list_to_dump, output_dump_file):
    if output_dump_file != None:
        output_dump_file = os.path.join(os.path.dirname(__file__), output_dump_file)
        print('Writing list to file: {}...'.format(output_dump_file))

    with open(output_dump_file, 'w') as output_file:
        for item in list_to_dump:
          output_file.write("%s\n" % item)

def fix_path(p):
    if not os.path.isabs(p):
        p = os.path.abspath(os.path.join(os.path.dirname(__file__), p))
    return p

def pickle_object(obj, pickle_file_path):
    f = open(pickle_file_path, 'wb')
    pickle.dump(obj, f)
    f.close()

def load_pickle(pickle_file_path):
    f = open(pickle_file_path, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
