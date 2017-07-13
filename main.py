
#exec(open('C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_sw_causes\\setup.py').read())

import os
setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import datetime
import maude_nlp

start_time = datetime.datetime.now()
print('Experiment starting at {}'.format(start_time))

print ('Creating models...')
classifiers, most_common_positive_words = maude_nlp.create_models()

print ('Classifying text...')
maude_nlp.classify(classifiers, most_common_positive_words)

end_time = datetime.datetime.now()

print('Experiment completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


