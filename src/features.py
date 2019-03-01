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

    print('The dataset consists of {} sentences'.format(len(train_sents)))
    return train_sents

def check_features(train_sents, model_name):
    for sent in train_sents:
        for word in sent:
            if model_name == "f" and (len(word) == 2 or len(word) == 11): return True
            elif (model_name == "fg" or model_name == "fgl") and len(word) == 11: return True
            else:
                return False

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


def word2features(sent, i, model_name, similarity):
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


def sent2features(sent, model_name, similarity):
    return [word2features(sent, i, model_name, similarity) for i in range(len(sent))]

def sent2labels(sent):
    return [sent[i][1] for i in range(len(sent))]
