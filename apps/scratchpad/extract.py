import os
import io
import sys

def extract():
    input_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\data\verified_positive_records.txt'
    output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\data\verified_positive_records_lcd.txt'
    keyword = 'LCD'
    total_lines_count = 0
    extracted_lines_count = 0

    print('Extracting all records matching \'{}\' from {}'.format(keyword, input_file))
    print ('Output file will be: {}'.format(output_file))

    if not os.path.exists(input_file):
        print ('ERROR - Input file does not exist: {}'.format(input_file))
        return

    with open(output_file, 'w') as fout:
        with open(input_file, 'r') as fin:
            remaining_records = []
            for line in fin:
                total_lines_count += 1
                print ('Looking at line {}...'.format(total_lines_count))
                if keyword in line:
                    print ('MATCHED: {}...'.format(line))
                    fout.write(line)
                    extracted_lines_count += 1
                else:
                    remaining_records.append(line)
               

    remaining_lines_count = 0
    with open(input_file, 'w') as fout:
        for line in remaining_records:
            fout.write(line)
            remaining_lines_count += 1


    print ('Extracted {} records from total {}. Remaining: {}.'.format(extracted_lines_count, total_lines_count, remaining_lines_count))


extract()