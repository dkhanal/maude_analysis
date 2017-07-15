# By Deepak Khanal
# dkhanal@gmail.com

import os
import random
import config
from foi_text import FoiTextRow

def get_known_positives(data_files, max = None):
    return get_known_dataset(data_files, is_positive, 'positive', True, max)

def get_known_negatives(data_files, max = None):
    return get_known_dataset(data_files, is_negative, 'negative', True, max)

def get_known_dataset(data_files, predicate, label, skip_first_line=True, max = None):
    print('Getting all known {} rows (max={})...'.format(label, max))

    all_rows = []
    for file in data_files:
        all_rows += get_matching_records_from_file(file, predicate, label, skip_first_line)

    random.shuffle(all_rows)

    return [r.mdr_report_key + '|' + r.mdr_text_key + '|' + r.foi_text for r in all_rows[:max]]



def get_matching_records_from_file(file, predicate, label, skip_first_line=True):
    print('Getting known {} rows from file: {}...'.format(label, file))

    if not os.path.isabs(file):
        file = os.path.join(os.path.dirname(__file__), file)
        print('Full path is: {}...'.format(file))

    file_name = os.path.basename(file)
    total_lines = 0
    rows = []
    percent = None
    with open(file) as f:
        for line in f:
            total_lines += 1
            if total_lines == 1 and skip_first_line:
                continue
            if config.data_file_max_num_rows_for_featureset != None and total_lines > config.data_file_max_num_rows_for_featureset:
               break;

            row = FoiTextRow(line=line)
            rows_length = len(rows)
            lines_so_far = total_lines -1
            percent = round(rows_length / lines_so_far * 100, 2)

            if config.verbose == True or total_lines % 10000 == 0:
                print('{}=>, {} {} records in total {} ({}%) so far. Checking row (report key: {} text key {})...'.format(file_name, rows_length, label, lines_so_far, percent, row.mdr_report_key, row.mdr_text_key))

            if predicate(row):
                rows.append(row)

        print('{}=>, {} {} records in total {} ({}%).'.format(file_name, len(rows), label, total_lines, percent))
        return rows

def is_positive(row):
    positive_bigrams = get_positive_bigrams()    
    return any(term in row.foi_text.upper() for term in positive_bigrams)

def get_positive_bigrams():
   return config.known_positive_signals


def is_negative(row):
    return not any(term in row.foi_text.upper() for term in config.potential_positive_signals)

