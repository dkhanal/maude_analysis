# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import pickle
import logging

def pickle_object(obj, pickle_file_path):
    logging.info('Pickling object as {}..'.format(pickle_file_path))
    f = open(pickle_file_path, 'wb')
    pickle.dump(obj, f)
    f.close()

def load_pickle(pickle_file_path):
    logging.info('Loading pickled object from {}..'.format(pickle_file_path))
    f = open(pickle_file_path, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
