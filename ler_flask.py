import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from pynif import NIFCollection
from ler_blstm import ler_tagger

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'nif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# generate links for each class (coarse- and fine-grained)
def add_class(tag):
    if tag[2:] == 'PER': return "http://dbpedia.org/ontology/Person"
    elif tag[2:] == 'AN': return "http://dbpedia.org/ontology/Lawyer"
    elif tag[2:] == 'RR': return "http://dbpedia.org/ontology/Judge"
    elif tag[2:] == 'LOC': return "http://dbpedia.org/ontology/Location"
    elif tag[2:] == 'LD': return "http://dbpedia.org/ontology/Country"
    elif tag[2:] == 'ST': return "http://dbpedia.org/ontology/City"
    elif tag[2:] == 'STR': return "http://dbpedia.org/ontology/Street"
    elif tag[2:] == 'LDS': return "http://dbpedia.org/ontology/Place"
    elif tag[2:] == 'ORG': return "http://dbpedia.org/ontology/Organisation"
    elif tag[2:] == 'UN': return "http://dbpedia.org/ontology/Company"
    elif tag[2:] == 'INN': return "http://dbpedia.org/ontology/GovernmentAgency"
    elif tag[2:] == 'GRT': return "http://dbpedia.org/ontology/TEXT"
    elif tag[2:] == 'MRK': return "http://dbpedia.org/ontology/brand"
    elif tag[2:] == 'NRM': return "http://dbpedia.org/ontology/TEXT"
    elif tag[2:] == 'GS': return "http://dbpedia.org/ontology/Law"
    elif tag[2:] == 'VO': return "http://dbpedia.org/ontology/TEXT"
    elif tag[2:] == 'EUN': return "http://dbpedia.org/ontology/TEXT"
    elif tag[2:] == 'REG': return "http://dbpedia.org/class/yago/TEXT"
    elif tag[2:] == 'VT': return "http://dbpedia.org/class/yago/Contract106520944"
    elif tag[2:] == 'VS': return "http://dbpedia.org/ontology/TEXT"
    elif tag[2:] == 'RS': return "http://dbpedia.org/ontology/LegalCase"
    elif tag[2:] == 'LIT': return "http://dbpedia.org/ontology/TEXT"
    else: print("Error: Invalid label", tag)


def write_nif(nif_text, predicted):
    nif = NIFCollection.loads(nif_text, format='turtle')
    if len(nif.contexts) == 1: 
        context = nif.contexts[0]
        text = nif.contexts[0].mention.strip()

    idx = 0
    previos_tag = ""
    start_idx = 0
    end_idx = 0
    for sentence in predicted:
        for token, ler_class in sentence:

            # check the whitespace
            if token != text[idx : idx + len(token)]:
                idx += 1
            
            # if match
            if token == text[idx : idx + len(token)]:

                if ler_class != "O":
                    
                    # for entities one after another
                    if previos_tag != "O" and previos_tag != "" and previos_tag[2:] != ler_class[2:]:
                        context.add_phrase(beginIndex=start_idx, endIndex=end_idx, taClassRef=[add_class(previos_tag)])

                    # for begin of new entity, set start index
                    elif previos_tag == "O": start_idx = idx
                    
                    # set end index
                    end_idx = idx + len(token)
                    
                    # check the last token
                    if end_idx == len(text): 
                        context.add_phrase(beginIndex=start_idx, endIndex=end_idx, taClassRef=[add_class(ler_class)])
                    
                    previos_tag = ler_class
                
                else:
                    # check if entity ends
                    if previos_tag != "O": 
                        context.add_phrase(beginIndex=start_idx, endIndex=end_idx, taClassRef=[add_class(previos_tag)])
                    
                    previos_tag = "O"

                idx += len(token)

    # generate annotated nif text
    nif = nif.dumps(format='turtle')
    return nif


@app.route('/ner', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        _file = request.files['file']
        if _file and os.path.splitext(_file.filename)[1][1:] in ALLOWED_EXTENSIONS: # os.path.splitext leaves dot in, hence the [1:]
            filename = secure_filename(_file.filename)
            _file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as f: text = f.read()
        ler_tagger(text, mode="-nif", modelPath="models/MODEL_NAME.h5")
        nif = write_nif(text, sentences)
        
    return nif