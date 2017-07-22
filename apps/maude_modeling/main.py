import sys
import os

setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import datetime
import config
import modeler


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    print('Model generation starting at {}'.format(start_time))
    
    input_data_files = config.input_data_file_sets
    if len(args) > 0:
        print('Generating model(s) for {}'.format(args[0]))
        input_data_files = [s for s in config.input_data_file_sets if args[0] in s['name']]
    modeler.create_models(input_data_files)

    end_time = datetime.datetime.now()
    print('Model generation completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

if __name__ == "__main__":
    main()
