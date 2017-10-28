# Copyright (c) 2017 Deepak Khanal
# All Rights Reserved
# dkhanal AT gmail DOT com

import classifier

def classify(line, models):
    if models is None or len(models) == 0:
        return None

    return classifier.classify_record(line, models)
