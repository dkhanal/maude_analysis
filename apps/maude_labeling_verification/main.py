import sys
import os

setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import os
import datetime
import config
import verifier


def main(args=None):
    os.system('mode con: cols=200 lines=50')

    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    print('Manually verifying auto-labeled known positive and known negative records starting at {}'.format(start_time))
    
    if len(args) == 0 or (args[0] != 'pos' and args[0] != 'neg'):
        print('Usage: python main.py [pos|neg]')
        return
                         
    print('Extracting for {}'.format(args[0]))

    verifier.verify_labels(args[0])

    end_time = datetime.datetime.now()
    print('Manual extraction completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

if __name__ == "__main__":
    main()
