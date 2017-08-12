import sys
import os
import re

base_path = os.path.dirname(__file__)
lib = os.path.join(base_path, 'lib')

if lib not in sys.path:
    print('Adding to sys.path: {}'.format(lib))
    sys.path.append(lib)
else:
    print('Already in sys.path: {}'.format(lib))

env_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.setenv.py'))
if os.path.isfile(env_script_path):
    script = open(env_script_path)
    exec(script.read())
else:
    print ('WARN: No environment variables set (.setenv.py not found). Configuration may be incomplete.')

import datetime
import config
import util
import util_azure


def main(args=None):
    print ('-- Uploader -- ')
    print ('Usage python upload.py [all]')
    if args is None:
        args = sys.argv[1:]

    output_dir = 'out'
    all = len(args) > 1 and args[1].lower() in 'all'

    output_files = config.output_files

    files_to_upload = [
        util.fix_path(output_files['verified_positive_records_file']),
        util.fix_path(output_files['verified_negative_records_file']),
        util.fix_path(output_files['last_processed_record_number_file'])
        ]

    if all == True:
        files_to_upload += [
        util.fix_path(output_files['potential_positive_records_blob']),
        util.fix_path(output_files['potential_negative_records_blob'])
        ]

    print (files_to_upload)
    print('Upload these files? [y/n] ')
    upload_confirmation = util.get_char_input()
    if not isinstance(upload_confirmation, str):
        upload_confirmation = bytes.decode(upload_confirmation)
    if upload_confirmation == 'y':
        util_azure.upload_files(files_to_upload, config.cloud_files['container'])

if __name__ == "__main__":
    main()
