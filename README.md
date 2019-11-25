# Legal-Entity-Recognition
## Fine-grained Named Entity Recognition in Legal Documents

This work has been partially funded by the project Lynx, which has received funding from the EU's Horizon 2020 research and innovation programme under grant agreement no.~780602, see [http://www.lynx-project.eu](http://lynx-project.eu/).

# Dataset of Legal Documents

Court decisions from 2017 and 2018 were selected for the dataset, published online by the [Federal Ministry of Justice and Consumer Protection](http://www.rechtsprechung-im-internet.de). The documents originate from seven federal courts: Federal Labour Court (BAG), Federal Fiscal Court (BFH), Federal Court of Justice (BGH), Federal Patent Court (BPatG), Federal Social Court (BSG), Federal Constitutional Court (BVerfG) and Federal Administrative Court (BVerwG). 

## Size

The dataset consists of 66,723 sentences with 2,157,048 tokens. The sizes of the seven court-specific datasets varies between 5,858 and 12,791 sentences, and 177,835 to 404,041 tokens. The distribution of annotations on a per-token basis corresponds to approx.~19--23 %. The Federal Patent Court (BPatG) dataset contains the lowest number of annotated entities (10.41 %).

|                          | LER       |
|--------------------------|-----------|
| Token mit Satzzeichen    | 2.157.048 |
| Token ohne Satzzeichen   | 1.868.355 |
| Sätze                    | 66.723    |
| Verteilung der Entitäten | 19,15 %   |

## Distribution of Entities

The dataset includes two different versions of annotations, one with a set of 19 fine-grained semantic classes and another one with a set of 7 coarse-grained classes. There are 53,632 annotated entities in total, the majority of which (74.34 %) are legal entities, the others are person, location and organization (25.66 %).

| Klasse | Bezeichnung        | Anzahl | Verteilung |
|--------|--------------------|--------|------------|
| **PER**    | Personen           | 1.747  | 3,26 %     |
| **AN**     | Anwälte            | 111    | 0,21 %     |
| **RR**     | Richter            | 1.519  | 2,83 %     |
| **LD**     | Länder             | 1.429  | 2,66 %     |
| **ST**     | Städte             | 705    | 1,31 %     |
| **STR**    | Straßen            | 136    | 0,25 %     |
| **LDS**    | Landschaften       | 198    | 0,37 %     |
| **ORG**    | Organisationen     | 1.166  | 2,17 %     |
| **UN**     | Unternehmen        | 1.058  | 1,97 %     |
| **INN**    | Institutionen      | 2.196  | 4,09 %     |
| **GRT**    | Gerichte           | 3.212  | 5,99 %     |
| **MRK**    | Marken             | 283    | 0,53 %     |
| **GS**     | Gesetze            | 18.520 | 34,53 %    |
| **VO**     | Verordnungen       | 797    | 1,49 %     |
| **EUN**    | Europäische Normen | 1.499  | 2,79 %     |
| **VS**     | Vorschriften       | 607    | 1,13 %     |
| **VT**     | Verträge           | 2.863  | 5,34 %     |
| **RS**     | Rechtsprechungen   | 12.580 | 23,46 %    |
| **LIT**    | Literatur          | 3.006  | 5,60 %     |
|        | Anzahl Entitäten   | **53.632** | 100 %      |

## Output Format

The dataset is freely available under the [CC-BY 4.0 license](https://creativecommons.org/licenses/by/4.0/deed.en). The output format is CoNLL-2002. Each line consists of two columns separated by a space. The first column contains a token and the second a tag in IOB2 format. The sentence boundary is marked with an empty line.

| Token               | Tag   |
|---------------------|-------|
| Am                  | O     |
| 7.                  | O     |
| März                | O     |
| 2006                | O     |
| fand                | O     |
| ein                 | O     |
| Treffen             | O     |
| der                 | O     |
| saarländischen      | B-INN |
| Landesregierung     | I-INN |
| unter               | O     |
| Vorsitz             | O     |
| des                 | O     |
| Ministerpräsidenten | O     |
| Müller              | B-RR  |
| mit                 | O     |
| Vertretern          | O     |
| der                 | O     |
| Evangelischen       | B-ORG |
| Kirche              | I-ORG |
| im                  | I-ORG |
| Rheinland           | I-ORG |
| und                 | O     |
| der                 | O     |
| Evangelischen       | B-ORG |
| Kirche              | I-ORG |
| der                 | I-ORG |
| Pfalz               | I-ORG |
| statt               | O     |
| .                   | O     |

# CRF
## Models

- CRF-F with features `f`;
- CRF-FG with features und gazetteers `fg`;
- CRF-FGL with features, gazetteers and lookup table for word similarity `fgl`.

## Training

- install [sklearn-crfsuite](https://sklearn-crfsuite.readthedocs.io/en/latest/) and run (modelName=f|fg|fgl):
```
python crf.py modelName trainPath testPath
```

- Models are saved in `models/`.

# BiLSTM
## Models

- BiLSTM-CRF `crf`;
- BiLSTM-CRF with char embeddings from BiLSTM `blstm-crf`;
- BiLSTM-CNN-CRF with char embeddings from CNN `cnn-crf`.

## Training

- install [BiLSTM-CNN-CRF](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf);
- copy `blstm.py` to folder `emnlp2017-bilstm-cnn-crf/` choose a model (modelName=crf|blstm-crf|cnn-crf) and run:
```
python blstm.py modelName trainPath devPath testPath
```
- Models are saved in `models/`.

# Requirements

- [emnlp2017-bilstm-cnn-crf](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf)
- [sklearn-crfsuite](https://sklearn-crfsuite.readthedocs.io/en/latest/)
- [SoMaJo](https://github.com/tsproisl/SoMaJo)

#### Bitte zitieren:

```
@mastersthesis{mastersthesis,
  author       = {Elena Leitner}, 
  title        = {Eigennamen- und Zitaterkennung in Rechtstexten},
  school       = {Universität Potsdam},
  year         = 2019,
  address      = {Potsdam},
  month        = 2,}
```

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Lizenzvertrag" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" /></a><br />Dieses Werk ist lizenziert unter einer <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Namensnennung 4.0 International Lizenz</a>.
