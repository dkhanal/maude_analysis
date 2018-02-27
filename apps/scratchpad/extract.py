# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import io
import sys
import datetime

def extract(keywords, input_files, output_file):
    print('Extracting all records matching {} keywords from {} files'.format(len(keywords), len(input_files)))
    print ('Output file will be: {}'.format(output_file))

    overall_lines_count = 0
    overall_extracted_lines_count = 0
    with open(output_file, 'w', encoding='utf-8', errors='ignore') as fout:
        overall_extracted_lines_count = 0
        for input_file in input_files:
            lines_count = 0
            extracted_lines_count = 0
            print ('Looking in file {}...'.format(input_file))
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as fin:
                remaining_records = []
                for line in fin:
                    lines_count += 1
                    overall_lines_count += 1

                    extracted = False
                    for keyword in keywords:
                        if keyword.upper() in line.upper():
                            print ('MATCHED {} in {}...'.format(keyword, line))
                            fout.write(line)
                            extracted = True
                            extracted_lines_count += 1
                            overall_extracted_lines_count += 1
                            break;

                    if not extracted:
                        remaining_records.append(line)
               
            remaining_lines_count = 0
            with open(input_file, 'w',  encoding='utf-8', errors='ignore') as forig:
                for line in remaining_records:
                    forig.write(line)
                    remaining_lines_count += 1

            print ('Extracted {} records from total {} in {}. Remaining: {}.'.format(extracted_lines_count, lines_count, input_file, remaining_lines_count))
    print ('Extracted total {} records from {} records across all {} files.'.format(overall_extracted_lines_count, overall_lines_count, len(input_files)))

    return overall_extracted_lines_count


strong_positive_keywords = [
    'COMPUTER ANOMALY',
    'COMPUTER CRASH',
    'COMPUTER DEFECT',
    'COMPUTER ERROR',
    'COMPUTER FAIL',
    'COMPUTER FREEZE',
    'COMPUTER FROZE',
    'COMPUTER PROBLEM',
    'CORRUPT DATABASE',
    'CORRUPT HARD DRIVE',
    'CORRUPT SOFTWARE',
    'DATABASE ANOMALY',
    'DATABASE CORRUPT',
    'DATABASE DEFECT',
    'DATABASE ERROR',
    'DATABASE FAIL',
    'DATABASE PROBLEM',
    'DISPLAY FREEZE',
    'DISPLAY FROZE',
    'FILE CORRUPT',
    'HARD DISK FAIL',
    'HARD DRIVE CORRUPT',
    'HARD DRIVE ERROR',
    'HARD DRIVE FAIL',
    'MEMORY ERROR',
    'MOTHER BOARD ERROR',
    'MOTHER BOARD FAIL',
    'MOTHERBOARD ERROR',
    'MOTHERBOARD FAIL',
    'NETWORK DEFECT',
    'NETWORK ERROR',
    'NETWORK ISSUE',
    'NETWORK PROBLEM',
    'SCREEN FREEZE',
    'SCREEN FROZE',
    'SOFTWARE ANOMALY',
    'SOFTWARE BUG',
    'SOFTWARE CORRUPT',
    'SOFTWARE CRASH',
    'SOFTWARE DEFECT',
    'SOFTWARE ERROR',
    'SOFTWARE FAIL',
    'SOFTWARE FREEZE',
    'SOFTWARE FROZE',
    'SOFTWARE MALFUNCTION',
    'SOFTWARE PROBLEM',
    'SOFTWARE UPDATE FAIL',
    'SOFTWARE UPGRADE FAIL',
    'SYSTEM FILE ERROR',
    'USER INTERFACE CRASH',
    'USER INTERFACE DEFECT',
    'USER INTERFACE ERROR',
    'USER INTERFACE FAIL',
    'USER INTERFACE FREEZE',
    'USER INTERFACE FROZE',
    ]

input_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\masked\positive_seed_records.txt'
output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\masked\computer_caused_events.txt'

extract(strong_positive_keywords, [input_file], output_file)
