import os
import sys
import sklearn
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import pickle


def read_file(filename):
    train_sents = []
    file = open(filename, encoding='utf-8')
    sent = []
    for line in file.readlines():
        if line.strip() == '':
            train_sents.append(sent)
            sent = []
        else:
            line = line.strip().split(' ')
            sent.append(tuple(line))
            if len(line) == 2 and model_name != "f":
                print("Error: add gazetteers to dataset, see src/gazetteers.py")
                exit()

    print('The dataset consists of {} sentences'.format(len(train_sents)))
    return train_sents

#############################################################################################################################################
#
# Features
#
#############################################################################################################################################

def add_features(sent,idx,context,model_name,similarity):
    
    features = {
        
        # 1. word shape, case feature
        str(context) + '_word': sent[idx + context][0],
        str(context) + '_word.lower()': sent[idx + context][0].lower(),
        str(context) + '_word.isupper()': sent[idx + context][0].isupper(),
        str(context) + '_word.islower()': sent[idx + context][0].islower(),
        str(context) + '_word.istitle()': sent[idx + context][0].istitle(),
        str(context) + '_word.isdigit()': sent[idx + context][0].isdigit(),
        str(context) + '_word.isalpha()': sent[idx + context][0].isalpha(),
        str(context) + '_word.isalnum()': sent[idx + context][0].isalnum(),
        str(context) + '_word.camelCase()': (sent[idx + context][0].istitle() or 
                                        sent[idx + context][0].isupper() or 
                                        sent[idx + context][0].islower()),

        # suffixes
        str(context) + '_word[-1]': sent[idx + context][0][-1],
        str(context) + '_word[-2:]': sent[idx + context][0][-2:],
        str(context) + '_word[-3:]': sent[idx + context][0][-3:],
        
        # prefixes
        str(context) + '_word[:1]': sent[idx + context][0][:1],
        str(context) + '_word[:2]': sent[idx + context][0][:2],
        str(context) + '_word[:3]': sent[idx + context][0][:3],
    }

    # gazetteers
    if "fg" in model_name and context == 0:
        features.update({str(context) + '_person': True if sent[idx + context][2] == 'PERSON' else False,
                        str(context) + '_land': True if sent[idx + context][3] == 'LAND' else False,
                        str(context) + '_stadt': True if sent[idx + context][4] == 'STADT' else False,
                        str(context) + '_strasse': True if sent[idx + context][5] == 'STRASSE' else False,
                        str(context) + '_Landschaft': True if sent[idx + context][6] == 'LANDSCHAFT' else False,
                        str(context) + '_firma': True if sent[idx + context][7] == 'FIRMA' else False,
                        str(context) + '_gesetz': True if sent[idx + context][8] == 'GESETZ' else False,
                        str(context) + '_verordnung': True if sent[idx + context][9] == 'VERORDNUNG' else False,
                        str(context) + '_vorschrift': True if sent[idx + context][10] == 'VORSCHRIFT' else False})

    # word similarity
    if model_name == "fgl":
        features.update({str(context) + '_similarity1': similarity[sent[idx + context][0]][0].encode('utf-8') if sent[idx + context][0] in similarity.keys() else '',
            str(context) + '_similarity2': similarity[sent[idx + context][0]][1].encode('utf-8') if sent[idx + context][0] in similarity.keys() else '',
            str(context) + '_similarity3': similarity[sent[idx + context][0]][2].encode('utf-8') if sent[idx + context][0] in similarity.keys() else '',
            str(context) + '_similarity4': similarity[sent[idx + context][0]][3].encode('utf-8') if sent[idx + context][0] in similarity.keys() else ''})

    return features


def word2features(sent, i):
    features = {
        'bias': 1.0
    }
    features.update(add_features(sent,i,0,model_name,similarity))
    if i > 0: features.update(add_features(sent,i,-1,model_name,similarity))
    if i > 1: features.update(add_features(sent,i,-2,model_name,similarity))
    if i == 0: features['BOS'] = True
        
    if i < len(sent)-1: features.update(add_features(sent,i,1,model_name,similarity))
    if i < len(sent)-2: features.update(add_features(sent,i,2,model_name,similarity))
    if i == len(sent)-1: features['EOS'] = True
                
    return features

def word2labels(sent, i):
    features = {
        'label': 'O',
    }
    features.update({
        'label': sent[i][1],
        })
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [sent[i][1] for i in range(len(sent))]


#############################################################################################################################################
#
# evaluation
#
#############################################################################################################################################

def compute_precision(guessed_sentences, correct_sentences, labels):
    assert(len(guessed_sentences) == len(correct_sentences))

    confusion_matrix = {}
    confusion_matrix['total'] = {'correctCount': 0, 'count': 0, 'support': 0}

    # add all labels to confusion_matrix
    for label in labels:
        confusion_matrix[label] = {'correctCount': 0, 'count': 0, 'support': 0}

    # count correct and guessed labels
    for sentenceIdx in range(len(guessed_sentences)):
        guessed = guessed_sentences[sentenceIdx]
        correct = correct_sentences[sentenceIdx]
        assert(len(guessed) == len(correct))
        idx = 0
        while idx < len(guessed):
            if correct[idx][0] == 'B' and correct[idx][2:] in labels: #A new chunk starts
                confusion_matrix[correct[idx][2:]]['support'] +=1
                confusion_matrix['total']['support'] +=1
            if guessed[idx][0] == 'B'and guessed[idx][2:] in labels: #A new chunk starts
                ler_class = guessed[idx][2:]
                confusion_matrix[ler_class]['count'] +=1
                confusion_matrix['total']['count'] +=1
#                 count += 1
                
                if guessed[idx] == correct[idx]:
                    idx += 1
                    correctlyFound = True
                    
                    while idx < len(guessed) and guessed[idx][0] == 'I': #Scan until it no longer starts with I
                        if guessed[idx] != correct[idx]:
                            correctlyFound = False
                        if correct[idx][0] == 'B'and correct[idx][2:] in labels: #A new chunk starts
                            confusion_matrix[correct[idx][2:]]['support'] +=1
                            confusion_matrix['total']['support'] +=1
                        
                        idx += 1
                    
                    if idx < len(guessed):
                        if correct[idx][0] == 'I': #The chunk in correct was longer
                            correctlyFound = False
                        
                    
                    if correctlyFound:
                        confusion_matrix[ler_class]['correctCount'] +=1
                        confusion_matrix['total']['correctCount'] +=1
                else:
                    idx += 1
            else:  
                idx += 1

    # calculate precision (or recall)
    precision_list = []
    support_list = []
    for label in labels:
        precision = 0
        if confusion_matrix[label]['count'] > 0:
            precision = float(confusion_matrix[label]['correctCount']) / confusion_matrix[label]['count']
        precision_list.append(precision)
        support_list.append(confusion_matrix[label]['support'])
    precision = float(confusion_matrix['total']['correctCount']) / confusion_matrix['total']['count']
    precision_list.append(precision)
    support_list.append(confusion_matrix['total']['support'])
    return precision_list, support_list

def classification_report_strict(gold_labels_list, predictions_list, labels, output_format='terminal'):
    labels.append('total')
    predictions = predictions_list
    gold_labels = gold_labels_list
    prec, support = compute_precision(predictions, gold_labels, labels)
    rec, nonesupport = compute_precision(gold_labels, predictions, labels)

    if output_format=='terminal':
        print('{:11}{:12}{:12}{:12}{:18}'.format('class', 'precision', 'recall', 'f1', 'support'))
        for idx in range(len(labels)):
            value = prec[idx]+rec[idx]
            if not value: f1 = 0
            else: f1 = 2*prec[idx]*rec[idx]/value
            print('{:7}{:10.3f} %{:10.3f} %{:10.3f} %{:11}'.format(labels[idx], prec[idx]*100, rec[idx]*100, f1*100, support[idx]))
        print('\n\n')

def separator(number):
    shift = 0
    for i in range(3,len(number)):
        if i%3 == 0:
            number = number[:-i-shift] + ',' + number[-i-shift:]
            shift += 1
    return number


#############################################################################################################################################
#
# Training
#
#############################################################################################################################################

# check input
if len(sys.argv) < 4:
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

X_train = [sent2features(s) for s in train_sents]
y_train = [sent2labels(s) for s in train_sents]

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

# prepare features for test
test_sents = read_file(test)
X_test = [sent2features(s) for s in test_sents]
y_test = [sent2labels(s) for s in test_sents]

# evaluation
y_test_pred = crf.predict(X_test)
labels = ['PER', 'RR', 'AN', 'LD', 'ST', 'STR', 'LDS', 'ORG', 'UN', 'INN', 'GRT', 'MRK', 'GS', 'VO', 'EUN', 'VS', 'VT', 'RS', 'LIT']
classification_report_strict(y_test, y_test_pred, labels)
