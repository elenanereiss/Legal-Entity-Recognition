import os
import sys
import sklearn
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pickle

from src.features import read_file, check_features, sent2features, sent2labels
from src.gazetteers import add_gazetteers
from src.evaluation import classification_report_strict

#
# Training
#

# check input
if len(sys.argv) != 4:
    print("Usage: python crf.py modelName trainPath testPath")
    exit()

model_name = str(sys.argv[1])

train = str(sys.argv[2])
if not os.path.isfile(train):
    print("Error: train file does not appear to exist")
    exit()

test = str(sys.argv[3])
if not os.path.isfile(test):
    print("Error: test file does not appear to exist")
    exit()

# check model names
if model_name == "f" or model_name == "fg":
    similarity = dict()

elif model_name == "fgl":
    # prepare word similarity list
    f = open('gazetteers/200k_2d_wordlists.list', 'r', encoding='utf-8')
    similarity = dict()
    for line in f.readlines():
        line = line.strip().split('\t')
        similarity[line[0]] = (line[1],line[2],line[3],line[4])
    f.close()

else:
    print("Error: existing model names are (1) f, (2) fg, (3) fgl")
    exit()


# prepare features for train
train_sents = read_file(train)

# check gazetteers for train
if not check_features(train_sents, model_name): 
    if not os.path.isfile(train.replace(".", "_gaz.")):
        add_gazetteers(train)
    else: print("{} already exists, read the file...".format(train.replace(".", "_gaz.")))
    train_sents = read_file(train.replace(".", "_gaz."))

X_train = [sent2features(s, model_name, similarity) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]
train_sents = None

# hyperparameters
crf = sklearn_crfsuite.CRF(algorithm='lbfgs',
  c1=0.1,
  c2=0.1,
  max_iterations=100,
  all_possible_transitions=True)

print('Train model crf-{}'.format(model_name))
crf.fit(X_train, y_train)

# saving the model
print('Saving file as models/crt-{}.pkl'.format(model_name))
filename = 'models/crf-' + model_name + '.pkl'
pickle.dump(crf, open(filename, 'wb'))
X_train = None
y_train = None

#
# Test
#

# prepare features for test
test_sents = read_file(test)

# check gazetteers for test
if not check_features(test_sents, model_name): 
    if not os.path.isfile(test.replace(".", "_gaz.")):
        add_gazetteers(test)
    else: print("{} already exists, read the file...".format(test.replace(".", "_gaz.")))
    test_sents = read_file(test.replace(".", "_gaz."))

X_test = [sent2features(s, model_name, similarity) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]
test_sents = None

# evaluation
y_test_pred = crf.predict(X_test)
X_test = None

# labels in order PER, LOC, ORG... 
labels = ['PER', 'RR', 'AN', 'LD', 'ST', 'STR', 'LDS', 'ORG', 'UN', 'INN', 'GRT', 'MRK', 'GS', 'VO', 'EUN', 'VS', 'VT', 'RS', 'LIT']
classification_report_strict(y_test, y_test_pred, labels)