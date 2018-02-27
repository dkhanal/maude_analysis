# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import io
import sys
import datetime

def find_record(string_to_match, input_files, output_file):
    print('Searching for all records matching {} from {} files'.format(len(string_to_match), len(input_files)))
    print ('Output file will be: {}'.format(output_file))

    overall_lines_count = 0
    overall_extracted_lines_count = 0

    out_dir = os.path.dirname(output_file)
    print('Creating directory: {}'.format(out_dir))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        print('Directory: {} already exists.'.format(out_dir))


    with open(output_file, 'w', encoding='utf-8', errors='ignore') as fout:
        overall_match_count = 0
        for input_file in input_files:
            lines_count = 0
            print ('Looking in file {}...'.format(input_file))
            match_count = 0
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as fin:
                remaining_records = []
                for line in fin:
                    lines_count += 1
                    overall_lines_count += 1

                    extracted = False
                    if string_to_match.upper() in line.upper():
                        print ('MATCHED {} in {}...'.format(string_to_match, line))
                        fout.write(line)
                        match_count = match_count + 1
                        overall_match_count = overall_match_count + 1

            print ('Found {} records from total {} in {}.'.format(match_count, lines_count, input_file))
    print ('Found total {} records from {} records across all {} files.'.format(overall_match_count, overall_lines_count, len(input_files)))

    return overall_extracted_lines_count

corpus = [
    'foitext2007.txt',
    'foitext2008.txt',
    'foitext2009.txt',
    'foitext2010.txt',
    'foitext2011.txt',
    'foitext2012.txt',
    'foitext2012.txt',
    'foitext2013.txt',
    'foitext2014.txt',
    'foitext2015.txt',
    'foitext2016.txt'
    ]

corpus_dir = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives'
output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\scratchpad\out\find_record_output_{}.txt'.format(datetime.datetime.now().isoformat().replace(':', ''))


string_to_match = '7967243'
find_record(string_to_match, [os.path.join(corpus_dir, f) for f in corpus], output_file)