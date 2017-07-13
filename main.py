
#exec(open('C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_sw_causes\\setup.py').read())

import os
setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import maude_nlp

maude_nlp.run_experiment('sim')

print('Done')

