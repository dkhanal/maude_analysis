# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import os
import io
import sys
import datetime
import re

def get_sample_density():
    sample_files = [
        ('pos', r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\auto_labeled_records\autolabeled_positive_records.txt'),
        ('neg', r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\auto_labeled_records\autolabeled_negative_records.txt')
        ]

    population_files = [
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2007.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2008.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2009.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2010.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2011.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2012.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2013.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2014.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2015.txt',
        r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\maude_experiments\narratives\foitext2016.txt',
        ]

    sample_record_ids = {}

    sample_density_output_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\auto_labeled_records\sample_density.txt'

    print('Loading sample Ids into a set... ')
    total_samples = 0
    samples_in_this_file = 0
    for (label, sample_file) in sample_files:
        with open(sample_file, 'r', encoding='utf-8', errors='ignore') as fin:
            samples_in_this_file = 0
            for line in fin:
                record_id = line[:40].strip()

                if record_id in sample_record_ids:
                    print('******** WARN: DUPLICATE: {}\n'.format(line))

                sample_record_ids[record_id] = (label, None)
                samples_in_this_file += 1
                total_samples += 1
        print('Loaded {} samples from {}.'.format(samples_in_this_file, os.path.basename(sample_file)))
    print('Loaded total {} samples from {} files.'.format(len(sample_record_ids), len(sample_files)))

    yearly_lines_count = 0
    yearly_samples_count = 0
    yearly_neg_samples_count = 0
    yearly_pos_samples_count = 0
    overall_lines_count = 0 
    overall_samples_count = 0
    overall_pos_samples_count = 0
    overall_neg_samples_count= 0
    with open(sample_density_output_file, 'w', encoding='utf-8', errors='ignore') as fout:
        year_regex = re.compile(r'\d+')
        year = None
        for population_file in population_files:
            # if the year rolled over, write out the boundary
            if overall_lines_count > 0:
                msg = '{}|{}|NA|{}\n'.format(overall_lines_count, year, '********* YEAR END LINE. TOTAL LINES {}. SAMPLES: {} (POS: {}/{:.3f} NEG: {}/{:.3f}). Percent: {:.4f} ********'.format(yearly_lines_count, yearly_samples_count, yearly_pos_samples_count, yearly_pos_samples_count/yearly_samples_count, yearly_neg_samples_count, yearly_neg_samples_count/yearly_samples_count, yearly_samples_count/yearly_lines_count))
                print(msg)
                fout.write(msg)

            year = year_regex.search(os.path.basename(population_file)).group(0)
            yearly_lines_count = 0
            yearly_samples_count = 0
            yearly_neg_samples_count = 0
            yearly_pos_samples_count = 0
            print ('Looking in file {}...'.format(population_file))
            with open(population_file, 'r', encoding='utf-8', errors='ignore') as fin:
                for line in fin:
                    yearly_lines_count += 1
                    overall_lines_count += 1

                    if yearly_lines_count == 1:
                        msg = '{}|{}|NA|{}\n'.format(overall_lines_count, year, '********* YEAR BEGIN LINE ********')
                        print(msg)
                        fout.write(msg)

                    record_id = line[:40].strip()

                    if record_id in sample_record_ids:
                        if sample_record_ids[record_id][1] is not None:
                            fout.write('******** DUPLICATE: {}\n'.format(line))
                            continue

                        fout.write('{}|{}|{}|{}\n'.format(overall_lines_count, year, sample_record_ids[record_id][0], record_id))
                        sample_record_ids[record_id] = (sample_record_ids[record_id][0], year)
                        yearly_samples_count += 1
                        overall_samples_count += 1

                        if sample_record_ids[record_id][0] == 'pos':
                            overall_pos_samples_count += 1
                            yearly_pos_samples_count += 1
                        else:
                            overall_neg_samples_count += 1
                            yearly_neg_samples_count += 1

        msg = '{}|{}|NA|{}\n'.format(overall_lines_count, year, '********* YEAR END LINE. TOTAL LINES {}. SAMPLES: {} (POS: {}/{:.3f} NEG: {}/{:.3f}). Percent: {:.4f} ********'.format(yearly_lines_count, yearly_samples_count, yearly_pos_samples_count, yearly_pos_samples_count/yearly_samples_count, yearly_neg_samples_count, yearly_neg_samples_count/yearly_samples_count, yearly_samples_count/yearly_lines_count))
        print(msg)
        fout.write(msg)

        msg = '*********  ALL TOTAL LINES {}. ALL TOTAL SAMPLES: {}. Percent: {:.4f} POS: {}, NEG: {} ********'.format(overall_lines_count, overall_samples_count, overall_samples_count/overall_lines_count, overall_pos_samples_count, overall_neg_samples_count)
        print(msg)
        fout.write(msg)

        samples_with_no_year = [record_id for record_id in sample_record_ids if sample_record_ids[record_id][1] is None] 
        if len(samples_with_no_year) > 0:
            msg = '>>>  The following {} records did not belong to any year\n'.format(len(samples_with_no_year))
            print(msg)
            fout.write(msg)
            for record_id in samples_with_no_year:
                msg = '{}\n'.format(record_id)
                print(msg)
                fout.write(msg)

# Entry Point
get_sample_density()