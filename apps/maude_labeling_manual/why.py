import sys
import os
import re

setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import datetime
import config

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    
    if len(args) == 0:
        print ('Usage python why.py <Report or Text Record Number> [return_on_first_find=True]')
        return

    output_dir = 'out'
    return_on_first_find = len(args) > 1 and not args[1].lower() in ['false']

    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), output_dir))

    match_count = 0
    for filename in os.listdir(output_dir):
        if filename.endswith('.process.txt'): 
            print('Looking in: {}...'.format(filename))
            with open(os.path.join(output_dir, filename), 'r') as f:
                for line in f:
                    match = re.search(args[0], line, re.IGNORECASE)
                    if match is not None:
                        print('{}=> {}.'.format(filename, line))
                        match_count += 1
                        if return_on_first_find == True:
                            return
    if match_count == 0:
        print('Nothing found for: {}.'.format(args[0]))

if __name__ == "__main__":
    main()
