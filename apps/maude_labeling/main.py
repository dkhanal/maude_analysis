import sys
import os

setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import os
import datetime
import config
import labeler


def main(args=None):
    os.system('mode con: cols=200 lines=50')

    if args is None:
        args = sys.argv[1:]

    start_time = datetime.datetime.now()
    print('Manually verifying pre-labeled records starting at {}'.format(start_time))
    
    mode = None

    if len(args) > 0 and (args[0] == 'pos' or args[0] == 'pos?' or args[0] == 'neg' or args[0] == 'neg?'):
        mode = args[0]
        return
                         
    print('Labeling records. Mode: {}'.format(mode))

    labeler.label_records(mode)

    end_time = datetime.datetime.now()
    print('Manual verification session completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))

if __name__ == "__main__":
    main()
