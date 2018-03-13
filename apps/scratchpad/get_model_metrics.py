import sys  
import numpy
from numpy import genfromtxt
from sklearn import metrics
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt


def log(line):
    print(line)


def show_performance_metrics(expected, predicted):
    log(metrics.classification_report(expected, predicted))
    log('CONFUSION MATRIX:')
    log(metrics.confusion_matrix(expected, predicted))

def show_performance_vs_seed_data():
    classification_vs_seed_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\data\verification\Classification_vs_Seed_Records_LogReg.csv'
    classification_vs_seed_data = genfromtxt(classification_vs_seed_file, delimiter=',', names=True, dtype=None)
    show_performance_metrics(classification_vs_seed_data['LABEL_ACTUAL'], classification_vs_seed_data['LABEL_PREDICTED'])

def show_performance_vs_labeled_data():
    classification_vs_labeled_file = r'C:\Users\dkhan\Google Drive\Dissertation\Machine Learning\Results\final\data\verification\Classification_vs_Labeled_Records.csv'
    classification_vs_labeled_data = genfromtxt(classification_vs_labeled_file, delimiter=',', names=True, dtype=None)
    show_performance_metrics(classification_vs_labeled_data['LABEL_ACTUAL'], classification_vs_labeled_data['LABEL_PREDICTED'])

log ('Calculating model performance...')
log('')
log('Calculating model performance against ALL SEED DATA')
show_performance_vs_seed_data()

#log('')
#log('')
#log('Calculating model performance against ALL LABELED DATA')
#show_performance_vs_labeled_data()





