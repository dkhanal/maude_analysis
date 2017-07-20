import sys
import os

setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import datetime
import config
import bag_of_words


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    print('Starting classification at: {}'.format(start_time))
    
    bag_of_words.classify()

    end_time = datetime.datetime.now()
    print('Classification completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

if __name__ == "__main__":
    main()
