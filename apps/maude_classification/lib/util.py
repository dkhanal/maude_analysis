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

def zip_files(list_of_files, zip_file_path):    
    print('Zipping files as: {}'.format(zip_file_path))
    compressed_stream = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
    for source_file in list_of_files:
        file_base_name = os.path.basename(source_file)
        print('Compressing {}...'.format(file_base_name))
        compressed_stream.write(source_file, file_base_name)
    compressed_stream.close()

def unzip(zip_file_path, target_dir):
    compressed = zipfile.ZipFile(zip_file_path, 'r')
    compressed.extractall(target_dir)
    compressed.close()

