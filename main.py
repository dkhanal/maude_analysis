# By Deepak Khanal
# dkhanal@gmail.com

#exec(open('C:\\Users\\dkhan\\Google Drive\\Dissertation\\Machine Learning\\maude_sw_causes\\setup.py').read())

import os
setup_script = open(os.path.join(os.path.dirname(__file__), 'setup.py'))
exec(setup_script.read())

import datetime
import maude_nlp
import config


start_time = datetime.datetime.now()
print('Experiment starting at {}'.format(start_time))

classifiers = None
features_definition = None

if config.use_pickeled_models_if_present == True:
    classifiers = maude_nlp.load_pickled_models()
    features_definition = maude_nlp.load_pickled_features_definition()

if config.use_pickeled_models_if_present == False or len(classifiers) == 0 or len(features_definition) == 0:
    print ('Creating models...')
    classifiers, features_definition = maude_nlp.create_models()

    if config.pickle_models == True:
        maude_nlp.pickle_models(classifiers)
        maude_nlp.pickle_features_definition(features_definition)

print ('Classifying text...')
maude_nlp.classify(classifiers, features_definition)

end_time = datetime.datetime.now()

print('Experiment completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


