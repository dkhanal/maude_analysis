import io
import sys

def extract():
    input_file = 'C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_experiments\\data\\verified_negative_records.txt'
    output_file = 'C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_experiments\\data\\verified_negative_records_fALSE.txt'
    keyword = 'FALSE'
    total_lines_count = 0
    extracted_lines_count = 0

    print('Extracting all records matching \'{}\' from {}'.format(keyword, input_file))
    print ('Output file will be: {}'.format(output_file))

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