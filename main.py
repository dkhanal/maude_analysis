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
feature_words = None

if config.use_pickeled_models_if_present == True:
    classifiers = maude_nlp.load_pickled_models()
    feature_words = maude_nlp.load_pickled_feature_words()

if config.use_pickeled_models_if_present == False or len(classifiers) == 0 or len(feature_words) == 0:
    print ('Creating models...')
    classifiers, feature_words = maude_nlp.create_models()

    if config.pickle_models == True:
        maude_nlp.pickle_models(classifiers)
        maude_nlp.pickle_feature_words(feature_words)

print ('Classifying text...')
maude_nlp.classify(classifiers, feature_words)

end_time = datetime.datetime.now()

print('Experiment completed at {}. Total duration: {}.'.format(end_time, end_time - start_time))


