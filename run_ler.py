#!/usr/bin/python
# This scripts loads a pretrained model and a raw .txt files. It then performs sentence splitting and tokenization and passes
# the input sentences to the model for tagging. Prints the tokens and the tags in a CoNLL format to stdout
# Usage: python run_ler.py modelPath inputPath
# For pretrained models see docs/Pretrained_Models.md

from __future__ import print_function
from somajo import Tokenizer, SentenceSplitter
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

def ReadTXT(inputPath):
    with open(inputPath, 'r', encoding='utf8') as f: text = f.read()
    sentences = SentenceSplit(text)
    sentences = [{'tokens': sent} for sent in sentences]
    return sentences

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python run_ler.py modelPath inputPath")
        exit()

    modelPath = sys.argv[1]
    inputPath = sys.argv[2]


    # :: Load the model ::
    lstmModel = BiLSTM.loadModel(modelPath)

    # :: Read input ::
    sentences = ReadTXT(inputPath)
    addCharInformation(sentences)
    addCasingInformation(sentences)
    dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

    # :: Tag the input ::
    tags = lstmModel.tagSentences(dataMatrix)

    # :: Output to stdout ::
    for sentenceIdx in range(len(sentences)):
        tokens = sentences[sentenceIdx]['tokens']

        for tokenIdx in range(len(tokens)):
            tokenTags = []
            for modelName in sorted(tags.keys()):
                tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])

            print("%s\t%s" % (tokens[tokenIdx], "\t".join(tokenTags)))
        print("")