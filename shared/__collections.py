# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import logging
import __io

def dump_list_to_file(list_to_dump, output_dump_file):
    if output_dump_file != None:
        output_dump_file = __io.abspath(output_dump_file)
        logging.info('Writing list to file: {}...'.format(output_dump_file))

    with open(output_dump_file, 'w') as output_file:
        for item in list_to_dump:
          output_file.write("%s\n" % item)
