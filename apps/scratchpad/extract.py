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

negative_keywords = set([
    #'A GE SERVICE REP PERFORMED AN ON SITE INVESTIGATION. THE FAILURE COULD NOT BE DUPLICATED. THE SYSTEM WAS TESTED AND FOUND TO BE WORKING AS INTENDED AND PUT BACK INTO SERVICE',
    #'PRODUCED A POPPING SOUND',
    #'HIGH TECHNICAL FACTORS',
    #'VERTICAL LIFT',
    #'CASING ISSUE',
    #'LOSS OF PRIME',
    #'EXPOSED WIRE',
    #'WRONG INSULIN',
    #'TOO HIGH',
    #'INACCURAC',
    #'ISSUES DURING PRIME',
    #'PERFORM FLUOROSCOPY X-RAY',
    #'PERFORM X-RAY',
    #'BROKEN ALTERNATING CURRENT',
    #'HIGH VOLT',
    #'COAGUCHEK SYSTEM',
    #'POWER SUPPLY PS3',
    #'WIRES ARE VISIBLE',
    #'BIPOLAR FORCEPS INSTRUMENT',
    #'INACCURA',
    #'MOTOR ERROR',
    #'WOULD NOT PRODUCE X-RAYS',
    #'MAIN BATTER',
    #'REPLACE THE X-RAY TUBE',
    #'REPLACED THE X-RAY TUBE',
    #'REPLACE X-RAY TUBE',
    #'REPLACED X-RAY TUBE',
    #'REPLACED GENERATOR BATTERIES',
    #'ADJUSTED THE 5V POWER SUPPLY',
    #'LOSS OF PRIME',
    #'AIR BUBBLE',
    #'EXTERNAL HARD DRIVE',
    #'EXTERNAL HARD DISK',
    #'CAUGUCHECK',
    #'GAS MODULE',
    #'BLOOWN FUSE',
    #'DOOR ASSEMBLY',
    #'STRIP ISSUE',
    #'BATTERY COMP',
    #'BATTERY CHARG',
    #'HARDWARE ERROR',
    #'ENCODER',
    #'MOTOR ERROR',
    #'BLOOD GLUCOSE READING',
    #'BLOOD GLUCOSE LEVEL',
    #'(BG) LEVEL'
    #'LOW BLOOD GLUCOSE',
    #'HIGH BLOOD GLUCOSE',
    #'HIGH READ',
    #'LOW READ',
    #'BATTERY INDICATOR',
    #'CASING',
    #'DRIVE SUPPORT',
    #'CLAMP',
    #'BACKUP PUMP',
    #'POWER SUPPLY',
    #'TOOTH',
    #'TEETH',
    #'WORKS ONLY ON',
    #'BRAKE',
    #'CRACKS',
    #'KINKS',
    #'OCCLU',
    #'LEAK',
    #'TRANSFORMER',
    #'CONNECTOR ASSEMBLY',
    #'SENSOR ASSEMBLY',
    #'DOOR ASSEMBLY',
    #'COAGUCHEK',
    'BATTERY PACK'
    ])

negative_classified_files = [
    'foitext2007.txt.predicted.neg.txt',
    'foitext2008.txt.predicted.neg.txt',
    'foitext2009.txt.predicted.neg.txt',
    'foitext2010.txt.predicted.neg.txt',
    'foitext2011.txt.predicted.neg.txt',
    'foitext2012.txt.predicted.neg.txt',
    'foitext2012.txt.predicted.neg.txt',
    'foitext2013.txt.predicted.neg.txt',
    'foitext2014.txt.predicted.neg.txt',
    'foitext2015.txt.predicted.neg.txt',
    'foitext2016.txt.predicted.neg.txt',
    ]

positive_classified_files = [
    'foitext2007.txt.predicted.pos.txt',
    'foitext2008.txt.predicted.pos.txt',
    'foitext2009.txt.predicted.pos.txt',
    'foitext2010.txt.predicted.pos.txt',
    'foitext2011.txt.predicted.pos.txt',
    'foitext2012.txt.predicted.pos.txt',
    'foitext2012.txt.predicted.pos.txt',
    'foitext2013.txt.predicted.pos.txt',
    'foitext2014.txt.predicted.pos.txt',
    'foitext2015.txt.predicted.pos.txt',
    'foitext2016.txt.predicted.pos.txt',
    ]

positive_keywords = [
    'SOFTWARE',
    'FIRMWARE',
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
    'HANDLED COMPU'
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
    'HARD DISK FAIL',
    'HARD DRIVE FAIL',
    'REPLACED HARD DISK',
    'REPLACED HARD DRIVE',
    'REPLACED THE HARD DISK',
    'REPLACED THE HARD DRIVE',
    ' USB ',
    ' FLOPPY DISK ',
    ' FLOPPY DRIVE ',
    'FLASH DRIVE',
    'FLASH MEMORY',
    'FIRMWARE',
    'NETWORKING ISSUE',
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
    'EMPTY SCREEN',
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
    'LOGIC ERROR',
    'SCROLL',
    'BLACK BOX',
    'EVENT LOGS',
    'LOG FILE',
    'LOG FILE',
    'BUTTON ERROR',
    'PROGRAM'

    ]

negative_auto_labeled_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_auto_labeler\out\autolabeled_negative_records_after_manual_adjust_9.txt'
positive_auto_labeled_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_auto_labeler\out\autolabeled_positive_records_after_manual_adjust_9.txt'

classifier_out_dir = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\classification_classifier\out'
output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_auto_labeler\out\false_pos_extract_session_output{}.txt'.format(datetime.datetime.now().isoformat().replace(':', ''))

extract(negative_keywords, [positive_auto_labeled_file], output_file)
#extract(positive_keywords, [os.path.join(classifier_out_dir, file) for file in negative_classified_files], output_file)
#extract(negative_keywords, [os.path.join(classifier_out_dir, file) for file in positive_classified_files], output_file)
#extract(positive_keywords, [r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\apps\labeling_candidate_extractor\out\false_pos_extract_session_output.potential_neg.txt'], output_file)
