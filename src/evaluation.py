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
