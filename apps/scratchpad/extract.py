# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import io
import sys
import datetime

def extract(keywords, overall_output_file):
    input_dir = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_auto_labeler\out'
    input_files = [
        'extract_session_output2017-12-16T162125.315444.txt',
        ] 

    print('Extracting all records matching {} keywords from {} files'.format(len(keywords), len(input_files)))
    print ('Overall output file will be: {}'.format(overall_output_file))

    if not os.path.exists(input_dir):
        print ('ERROR - Input dir does not exist: {}'.format(input_dir))
        return

    extracted_lines_count = 0
    overall_extracted_lines_count = 0
    with open(overall_output_file, 'w', encoding='utf-8', errors='ignore') as fout:
        overall_extracted_lines_count = 0
        for input_file in input_files:
            overall_extracted_lines_count += extracted_lines_count
            total_lines_count = 0
            extracted_lines_count = 0
            print ('Looking in file {}...'.format(input_file))
            with open(os.path.join(input_dir, input_file), 'r', encoding='utf-8', errors='ignore') as fin:
                remaining_records = []
                for line in fin:
                    total_lines_count += 1

                    extracted = False
                    for keyword in keywords:
                        if keyword.upper() in line.upper():
                            print ('MATCHED {} in {}...'.format(keyword, line))
                            fout.write(line)
                            extracted = True
                            extracted_lines_count += 1
                            break;

                    if not extracted:
                        remaining_records.append(line)
               
            remaining_lines_count = 0
            with open(os.path.join(input_dir, input_file), 'w',  encoding='utf-8', errors='ignore') as forig:
                for line in remaining_records:
                    forig.write(line)
                    remaining_lines_count += 1

            print ('Extracted {} records from total {} in {}. Remaining: {}.'.format(extracted_lines_count, total_lines_count, input_file, remaining_lines_count))
    print ('Extracted total {} records from all files.'.format(overall_extracted_lines_count, keyword))

    return overall_extracted_lines_count

#keywords = [
#    'ATTORNEY',
#    'MAIN BATTERY',
#    'BATTERY COMPARTMENT',
#    'WOULD NOT PRODUCE X-RAY',
#    'MOTOR ERROR ALARM',
#    'ATTORNEY',
#    'ARCING',
#    'FILAMENT',
#    'BROKE OFF',
#    'BROKEN OFF',
#    'HIGH VOLTAGE',
#    'CASING',
#    'POWER SUPPLY',
#    'NO DELIVERY',
#    'BATTERY MALFUNCTION',
#    'LEGAL',
#    'LITIGATION',
#    'STRIP ISSUE',
#    'LAWYER']




keywords = [
    'SOFTWARE ISSUE',
    'SOFTWARE CRASH',
    'SOFTWARE PROBLEM',
    'SOFTWARE ERROR',
    'SOFTWARE DEFECT',
    'SOFTWARE ANOMALY',
    'SOFTWARE UPGRADE',
    'SOFTWARE UPDATE',
    'SOFTWARE RELOAD',
    'SOFTWARE PATCH',
    'SOFTWARE BUG',
    'SOFTWARE INSTALL',
    'SOFTWARE REINSTALL',
    'SOFTWARE RE-INSTALL',
    'SOFTWARE VERSION',
    'SOFTWARE MALFUNCTION',
    'SOFTWARE CORRUPT',
    'SOFTWARE DOES NOT',
    'SOFTWARE DID NOT',
    'SOFTWARE WAS NOT',
    'SOFTWARE DOWNLOAD',
    'SOFTWARE CONFIGURATION',
    'SOFTWARE UNEXPECTED',
    'UNEXPECTED SOFTWARE',
    'INCOMPATIBLE SOFTWARE',
    'SOFTWARE LIMIT',
    'SOFTWARE FILE',
    'SOFTWARE FREEZE',
    'SOFTWARE FROZE',
    'SOFTWARE FAIL',
    'SOFTWARE EXIT',
    'LANGUAGE FILE',
    'CALIBRATION FILE',
    'CONFIGURATION FILE',
    ' SYS FILE',
    'SYSTEM FILE',
    'DOWNLOAD SOFTWARE',
    'CORRUPT SOFTWARE',
    'CALCULATING SOFTWARE',
    'UPGRADED SOFTWARE',
    'RELOADED SOFTWARE',
    'RE-LOADED SOFTWARE',
    'INSTALLED SOFTWARE',
    'LIS SOFTWARE',
    'RE-INSTALLED SOFTWARE',
    'REINSTALLED SOFTWARE',
    'NEW SOFTWARE',
    'SOFTWARE REPLACE',
    'SOFTWARE INVESTIGA',
    'SOFTWARE EVAL',
    'SOFTWARE WAS UPDATE',
    'SOFTWARE WAS UPGRADED',
    'SOFTWARE WAS RELOADED',
    'SOFTWARE WAS RE-LOADED',
    'SOFTWARE WAS INSTALLED',
    'SOFTWARE WAS RE-INSTALLED',
    'SOFTWARE WAS REINSTALLED',
    'SOFTWARE APPEARS TO HAVE MALFUNCTIONED',
    'SOFTWARE WAS FOUND TO HAVE MALFUNCTIONED',
    'SINGLE BOARD COMPUTER',
    'COMPUTER WORKSTATION',
    'COMPUTER PCB',
    'COMPUTER ISSUE',
    'COMPUTER CRASH',
    'COMPUTER PROBLEM',
    'COMPUTER ERROR',
    'COMPUTER DEFECT',
    'COMPUTER ANOMALY',
    'COMPUTER REPLACE',
    'COMPUTER WAS REPLACE',
    'COMPUTER MALFUNCTION',
    'COMPUTER FREEZE',
    'COMPUTER WOULD FREEZE',
    'COMPUTER WAS FREEZE',
    'COMPUTER WAS FROZE',
    'COMPUTER HAD FROZE',
    'COMPUTER FROZE',
    'COMPUTER FAIL',
    'COMPUTER DISPLAY',
    'COMPUTER MONITOR',
    'COMPUTER UPGRADE',
    'COMPUTER RETURN',
    'COMPUTER CPU',
    'COMPUTER AND FLASH CARD',
    'COMPUTER AND FLASHCARD',
    'HANDHELD COMPUTER',
    'PROGRAMMING ISSUE',
    'PROGRAMMING PROBLEM',
    'PROGRAMMING ERROR',
    'PROGRAMMING DEFECT',
    'PROGRAMMING ANOMALY',
    'DATABASE ISSUE',
    'DATABASE PROBLEM',
    'DATABASE ERROR',
    'DATABASE DEFECT',
    'DATABASE ANOMALY',
    'DATABASE FAIL',
    'DATABASE CORRUPT',
    'CORRUPT DATABASE',
    'NETWORK ISSUE',
    'NETWORK PROBLEM',
    'NETWORK ERROR',
    'NETWORK DEFECT',
    'NETWORK ANOMALY',
    'HARD DISK',
    'HARD DRIVE',
    ' USB ',
    ' FLOPPY DISK ',
    ' FLOPPY DRIVE ',
    'FLASH DRIVE',
    'FLASH MEMORY',
    'FIRMWARE',
    'NETWORKING',
    ' WIFI ',
    ' SQL ',
    'TOUCHSCREEN',
    'TOUCH SCREEN',
    'SERIAL CABLE',
    'VGA CABLE',
    'ETHERNET',
    'ROUTER',
    'MOTHERBOARD',
    'MOTHER BOARD',
    'PROCESSOR BOARD',
    'USER INTERFACE BOARD',
    'GUI BOARD',
    'UI) BOARD',
    'OUTPUT PRINTED CIRCUIT BOARD',
    'I/O PCB',
    'IO PCB',
    'BLANK SCREEN',
    'BLACK SCREEN',
    'WHITE SCREEN',
    'WHITESCREEN',
    'BLUE SCREEN',
    'BLUESCREEN',
    'INCORRECT SETTINGS',
    'SETTINGS ISSUE',
    "DISPLAY ISSUE",
    "DISPLAY ERROR",
    "RANDOM ACCESS MEMORY",
    "DATA STORAGE",
    "DATA TRANSFER",
    ]


output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_auto_labeler\out\extract_session_output{}.txt'.format(datetime.datetime.now().isoformat().replace(':', ''))
extract(keywords, output_file)

