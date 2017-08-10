import os
import config
import util


def extract_records(input_files):
    print('Extracting known positive and negative records from {} file(s)...'.format(len(input_files)))

    positive_records_output_file = util.fix_path(config.positive_records_output_file)
    negative_records_output_file = util.fix_path(config.negative_records_output_file)
    last_processed_record_number_file = util.fix_path(config.last_processed_record_number_file)

    last_read_record_number = 0

    if os.path.exists(last_processed_record_number_file):
        with open(last_processed_record_number_file, 'r') as f:
            for line in f:
                last_read_record_number = int(line)

    with open(positive_records_output_file, 'a') as positive_records:
        with open(negative_records_output_file, 'a') as negative_records:
            for input_file in input_files:
                input_file_path = util.fix_path(input_file)
                with open(input_file_path, 'r') as f:
                    current_record_number = 0
                    for line in f:
                        current_record_number += 1
                        if current_record_number <= last_read_record_number:
                            continue

                        print ('')
                        print('Input File: {}'.format(os.path.basename(input_file_path)))
                        print('Output File (positive): {}'.format(os.path.basename(positive_records_output_file)))
                        print('Output File (negative): {}'.format(os.path.basename(negative_records_output_file)))
                        print('Record Number: {}'.format(current_record_number))
                        print ('')
                        print(line)
                        print ('')
                        print('[P]ositive, [N]egative, [U]nknown or [Q]uit? ')
                        decision = bytes.decode(util.get_char_input())
                        if decision == 'q' or decision == 'quit':
                            return

                        if decision == 'p' or decision == 'positive':
                            positive_records.write(line)
                        elif decision == 'n' or decision == 'negative':
                            negative_records.write(line)

                        with open(last_processed_record_number_file, 'w') as last_processed:
                            last_processed.write(str(current_record_number))
                        last_read_record_number = current_record_number


