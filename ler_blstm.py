#!/usr/bin/python
# This scripts loads a pretrained model and a raw .txt files. It then performs sentence splitting and tokenization and passes
# the input sentences to the model for tagging. Prints the tokens and the tags in a CoNLL format to stdout
# Usage: python RunModel.py modelPath inputPath
# For pretrained models see docs/Pretrained_Models.md
from __future__ import print_function
from somajo import Tokenizer, SentenceSplitter
from pynif import NIFCollection
from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM
import sys

# :: Tokenize German text ::
def SentenceSplit(text):

    tokenizer = Tokenizer(split_camel_case=False, token_classes=False, extra_info=False)
    tokens = tokenizer.tokenize(text)

    sentence_splitter = SentenceSplitter(is_tuple=False)
    sentences = sentence_splitter.split(tokens)
    return sentences

# :: Read the input ::
def ReadNIF(text):
    parsed_collection = NIFCollection.loads(text, format='turtle')
    if len(parsed_collection.contexts) == True:
        sentences = SentenceSplit(parsed_collection.contexts[0].mention)
        sentences = [{'tokens': sent} for sent in sentences]
        return sentences
    else: 
        print("Error: More mentions in NIF than one ")
        return []

def ReadTXT(text):
    sentences = SentenceSplit(text)
    sentences = [{'tokens': sent} for sent in sentences]
    return sentences

def ler_tagger(text, mode, modelPath):

    # :: Load the model ::
    lstmModel = BiLSTM.loadModel(modelPath)

    # :: Read input ::
    if mode == "-txt": 
        sentences = ReadTXT(text)
    elif mode == "-nif": 
        sentences = ReadNIF(text)
    else: 
        print("Invalid mode: {}. Valid modes are -txt or -nif.".format(mode))
        exit()

    addCharInformation(sentences)
    addCasingInformation(sentences)
    dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

    # :: Tag the input ::
    tags = lstmModel.tagSentences(dataMatrix)

    list = []
    for sentenceIdx in range(len(sentences)):
        tokens = sentences[sentenceIdx]['tokens']

        sent_list = []
        for tokenIdx in range(len(tokens)):
            tokenTags = []
            for modelName in sorted(tags.keys()):
                tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

            sent_list.append((tokens[tokenIdx], "\t".join(tokenTags)))
        list.append(sent_list)
    return list

if __name__ == '__main__': 
    if len(sys.argv) != 4:
        print("Usage: python RunLER.py -txt|nif modelPath inputPath")
        exit()

    mode = str(sys.argv[1])
    modelPath = sys.argv[2]
    inputPath = sys.argv[3]
    with open(inputPath, 'r') as f: text = f.read()

    sentences = ler_tagger(text, mode, modelPath)
    print (sentences)

# :: Output to stdout ::



#for sentenceIdx in range(len(sentences)):
#    tokens = sentences[sentenceIdx]['tokens']

#    for tokenIdx in range(len(tokens)):
#        tokenTags = []
#        for modelName in sorted(tags.keys()):
#            tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

#        print("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)))
#    print("")