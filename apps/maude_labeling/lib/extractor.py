import os
import re
import sys
import codecs
import datetime
import config
import platform
import uploader
import util

def extract_records(input_files, output_dir, max = None):    
    print('Extracting known positive and negative records from {} file(s)...'.format(len(input_files)))

    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), output_dir))

    util.dump_list_to_file(config.known_positive_records_qualifying_terms, os.path.join(output_dir,  'positive_qualifying_criteria.txt'))
    util.dump_list_to_file(config.known_positive_records_disqualifying_terms, os.path.join(output_dir,  'positive_disqualifying_criteria.txt'))
    
    total_positive_count = 0
    total_negative_count = 0
    
    for file_name in input_files:
        if file_name.endswith('.txt'): 
            print('Extracting known positive and negative records from {}...'.format(file_name))
            file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
            positive_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.pos.txt')
            negative_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.neg.txt')
            maybe_positive_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.maybe.pos.txt')
            maybe_negative_records_output_file = os.path.join(output_dir,  file_name_without_ext + '.maybe.neg.txt')

            process_log_file =  os.path.join(output_dir,  file_name_without_ext + '.process.txt')
            positive_count, negative_count = extract_matching_records_from_file(file_name, 
                                                                                positive_records_output_file, 
                                                                                negative_records_output_file, 
                                                                                maybe_positive_records_output_file,
                                                                                maybe_negative_records_output_file,
                                                                                process_log_file, 
                                                                                is_positive, 
                                                                                is_negative, 
                                                                                True, 
                                                                                max)
            total_positive_count += positive_count
            total_negative_count += negative_count

def extract_matching_records_from_file(input_file, 
                                       positive_records_output_file, 
                                       negative_records_output_file, 
                                       maybe_positive_records_output_file,
                                       maybe_negative_records_output_file,
                                       process_log_file, 
                                       positive_predicate, 
                                       negative_predicate, 
                                       skip_first_line=True,
                                       max=None):
    print('Extracting {} known positive and negative records from file: {}...'.format('ALL' if max == None else max, input_file))

    if not os.path.isabs(input_file):
        input_file = os.path.join(os.path.dirname(__file__), input_file)

    print('Positive records output path: {}...'.format(positive_records_output_file))
    print('Negative records output path: {}...'.format(negative_records_output_file))
    print('Process log path: {}...'.format(process_log_file))

    file_name = os.path.basename(input_file)
    total_lines = 0
    total_data_lines = 0
    total_positive_data_lines = 0
    total_negative_data_lines = 0
    positive_out_file = open(positive_records_output_file, 'w')
    maybe_positive_out_file = open(maybe_positive_records_output_file, 'w')
    negative_out_file = open(negative_records_output_file, 'w')
    maybe_negative_out_file = open(maybe_negative_records_output_file, 'w')
    qualification_process_log_file_handle = open(process_log_file, 'w')
    start_time = datetime.datetime.now()
    process_log_first_line = 'MAUDE Labeling Process Log. Computer: {}. OS: {} {}  Date/Time: {}. Python Version: {}\n'.format(platform.node(), platform.system(), platform.release(), start_time, sys.version)
    qualification_process_log_file_handle.write(process_log_first_line)
    fin = codecs.open(input_file, encoding='utf-8', errors='ignore')
    for line in fin:
        sys.stdout.write("POS: {} NEG: {}. Now looking at record: {}... \r".format(total_positive_data_lines, total_negative_data_lines, total_data_lines))
        sys.stdout.flush()
        total_lines += 1
        if total_lines == 1 and skip_first_line:
            continue
        if max is not None and total_positive_data_lines >= max and total_negative_data_lines >= max:
            break;

        total_data_lines += 1

        if (max is None or total_positive_data_lines < max) and positive_predicate(line, maybe_positive_out_file, qualification_process_log_file_handle):
            positive_out_file.write(line)
            total_positive_data_lines += 1
            pass
        elif (max is None or total_negative_data_lines < max) and negative_predicate(line, maybe_negative_out_file, qualification_process_log_file_handle):
            negative_out_file.write(line)
            total_negative_data_lines += 1
            pass

        if config.verbose == True or total_lines % 10000 == 0:
            positive_percent = round(total_positive_data_lines / total_data_lines * 100, 2)
            negative_percent = round(total_negative_data_lines / total_data_lines * 100, 2)
            print('{}=>, {} ({}%) positive and {} ({}%) negative records in total {} records so far...'.format(file_name, total_positive_data_lines, positive_percent, total_negative_data_lines, negative_percent, total_data_lines))

    positive_percent = round(total_positive_data_lines / total_data_lines * 100, 2)
    negative_percent = round(total_negative_data_lines / total_data_lines * 100, 2)
    message = '{}=>, {} ({}%) positive and {} ({}%) negative records in the {} records examined in this file'.format(file_name, total_positive_data_lines, positive_percent, total_negative_data_lines, negative_percent, total_data_lines)
    print(message)
    qualification_process_log_file_handle.write(message + '\n')
    end_time = datetime.datetime.now()
    qualification_process_log_file_handle.write('Labeling completed at {}. Duration: {} \n'.format(end_time, end_time - start_time))
    fin.close()
    positive_out_file.close()
    maybe_positive_out_file.close()
    negative_out_file.close()
    maybe_negative_out_file.close()
    qualification_process_log_file_handle.close()

    if config.upload_output_to_cloud == True:
        list_of_files_to_upload = [positive_records_output_file,
                                   negative_records_output_file,
                                   maybe_positive_records_output_file,
                                   maybe_negative_records_output_file,
                                   process_log_file]
        uploader.upload_files(list_of_files_to_upload, os.path.dirname(positive_records_output_file) , os.path.join(os.path.dirname(positive_records_output_file), os.path.splitext(file_name)[0]+'.zip'))

    return (total_positive_data_lines, total_negative_data_lines)

def is_positive(line, questionable_records_file, qualification_process_log_file_handle):
    likely_positive = False
    for pattern in config.known_positive_records_qualifying_terms:
        match = re.search(pattern, line, re.IGNORECASE)
        if match is not None:
            likely_positive = True
            qualification_process_log_file_handle.write(line[:50] + '... POSITIVE MATCHED ON: ' + match.group() + '\n')
            break

    if likely_positive == False:
        return False

    for pattern in config.known_positive_records_disqualifying_terms:
        match = re.search(pattern, line, re.IGNORECASE)
        if match is not None:
            questionable_records_file.write(line)
            qualification_process_log_file_handle.write(line[:50] + '... POSITIVE MATCHED BUT DISQUALIFIED DUE TO  MATCH ON: ' + match.group() + '\n')
            return False

    return True

def is_negative(line, questionable_records_file, qualification_process_log_file_handle):
    for pattern in config.potential_positive_records_qualifying_terms:
        match = re.search(pattern, line, re.IGNORECASE)
        if match is not None: # No match found on any potential signals
            questionable_records_file.write(line)
            qualification_process_log_file_handle.write(line[:50] + '... LIKELY NEGATIVE BUT DISQUALIFIED DUE TO MATCH ON: ' + match.group() + '\n')
            return False

    return True