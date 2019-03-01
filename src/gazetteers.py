import os
import sys
from somajo import Tokenizer

def read_dataset(filename):
    sentences = []
    sentence = []
    label = []
    labels = []
    f = open(filename, 'r',  encoding='utf-8')
    for line in f.readlines():
        line = line.strip()
        if not line:
            if len(sentence) > 0:
                sentences.append(sentence)
                labels.append(label)
                sentence = []
                label = []
        else:
            word = line.split(' ')
            assert len(word) >= 2
            sentence.append(word[0])
            label.append(word[1])
    if len(sentence) > 0:
        sentences.append(sentence)
        labels.append(label)
    f.close()
    return sentences, labels

def build_list(filename):
    tokenizer = Tokenizer(split_camel_case=False, token_classes=False, extra_info=False)
    gazetteers = set()
    f = open(filename, 'r', encoding='utf-8')
    for line in f.readlines(): 
        gazetteers.add(' '.join(tokenizer.tokenize(line.strip())))
    f.close()
    print('read {}'.format(filename))
    return gazetteers

def add_labels(sentences, gazetteers, label_name):
    labels_list = []
    labels = []
    for sentence in sentences:

        for idx in range(len(sentence)):
            
            word = sentence[idx]
            if word in gazetteers: 
                labels.append(label_name)
            else: labels.append('O')
            if idx != 0: 
                for reverse_idx in range(idx):
                    word = sentence[idx-reverse_idx - 1] + ' ' + ' '.join(sentence[idx-reverse_idx:idx+1])
                    if word in gazetteers:

                        for reverse_idx in range(len(word.split(' ')) + 1):
                            labels[idx-reverse_idx] = label_name
                        break

        # check size of labels
        assert(len(labels) == len(sentence))
        labels_list.append(labels)
        labels = []
    print('search for {} in list'.format(label_name))

    # check size of list of labels
    assert(len(labels_list) == len(sentences))
    return labels_list


def add_gazetteers(path):
    print("Prepare gazetteers for train")

    # classes
    PER = build_list('gazetteers/personennamen.list')
    LD = build_list('gazetteers/laendernamen.list')
    ST = build_list('gazetteers/stadtnamen.list')
    STR = build_list('gazetteers/strassennamen.list')
    LDS = build_list('gazetteers/landschaftsbezeichnungen.list')
    UN = build_list('gazetteers/firmennamen.list')
    GS = build_list('gazetteers/gesetzesnamen.list')
    VO = build_list('gazetteers/verordnungsnamen.list')
    VS = build_list('gazetteers/vorschriftennamen.list')
    sentences, labels = read_dataset(path)


    # lists
    PER_list = add_labels(sentences, PER, 'PERSON')
    LD_list = add_labels(sentences, LD, 'LAND')
    ST_list = add_labels(sentences, ST, 'STADT')
    STR_list = add_labels(sentences, STR, 'STRASSE')
    LDS_list = add_labels(sentences, STR, 'LANDSCHAFT')
    UN_list = add_labels(sentences, UN, 'FIRMA')
    GS_list = add_labels(sentences, GS, 'GESETZ')
    VO_list = add_labels(sentences, VO, 'VERORDNUNG')
    VS_list = add_labels(sentences, VS, 'VORSCHRIFT')
    print('\n')

    # write
    filename = path.replace('.', '_gaz.')
    f = open(filename, 'w', encoding='utf-8')
    for sentence_idx in range(len(sentences)):
        for word_idx in range(len(sentences[sentence_idx])):
            f.write('{} {} {} {} {} {} {} {} {} {} {}\n'.format(sentences[sentence_idx][word_idx],
                                                                labels[sentence_idx][word_idx],
                                                                PER_list[sentence_idx][word_idx],
                                                                LD_list[sentence_idx][word_idx],
                                                                ST_list[sentence_idx][word_idx],
                                                                STR_list[sentence_idx][word_idx],
                                                                LDS_list[sentence_idx][word_idx],
                                                                UN_list[sentence_idx][word_idx],
                                                                GS_list[sentence_idx][word_idx],
                                                                VO_list[sentence_idx][word_idx],
                                                                VS_list[sentence_idx][word_idx]))
        f.write('\n')
    f.close()
    print("File saved as {}".format(path.replace(".","_gaz.")))
