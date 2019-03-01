# Legal-Entity-Recognition
## Eigennamen- und Zitaterkennung in Rechtstexten

Die vorliegende Arbeit ist im Rahmen des [Lynx-Projektes](http://lynx-project.eu/) H20H20 am [DFKI](https://www.dfki.de/web/) entstanden.


# Juristisches Korpus

Das Korpus besteht aus 750 Entscheidungen der Jahre 2017-2018, die vom Bundesministerium der Justiz und für Verbraucherschutz auf dem Portal ['Rechtsprechung im Internet'](http://www.rechtsprechung-im-internet.de) veröffentlicht wurden. Die Entscheidungen stammen aus sieben Bundesgerichten: Bundesarbeitsgericht (BAG), Bundesfinanzhof (BFH), Bundesgerichtshof (BGH), Bundespatentgericht (BPatG), Bundessozialgericht (BSG), Bundesverfassungsgericht (BVerfG) und Bundesverwaltungsgericht (BVerwG).

## Korpusgröße

|                          | LER       |
|--------------------------|-----------|
| Token mit Satzzeichen    | 2.157.048 |
| Token ohne Satzzeichen   | 1.868.355 |
| Sätze                    | 66.723    |
| Verteilung der Entitäten | 19,15 %   |

## Verteilung der Klassen

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

## Datenformat
Das Korpus steht im CoNLL-2002-Format zur Verfügung. Die Daten sind in zwei Spalten aufgeteilt, die mit einem Leerzeichen getrennt sind. Jedes Wort befindet sich in einer Zeile. Die Satzgrenze ist mit einer leeren Zeile markiert. Die erste Spalte enthält ein Wort und die zweite ein Tag im IOB2-Format.

| Wort                | Tag   |
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
## Modelle

- CRF-F mit Features `f`;
- CRF-FG mit Features und Gazetteers `fg`;
- CRF-FGL mit Features, Gazetteers und Lookup-Tabelle für die Wortähnlichkeit `fgl`.

## Training
- [sklearn-crfsuite](https://sklearn-crfsuite.readthedocs.io/en/latest/) installieren und ausführen:
```
python crf.py modelName trainPath testPath
```

- Modelle werden in `models/` gespeichert.

# BLSTM
## Modelle

- BLSTM-CRF `crf`;
- BLSTM-CRF mit Buchstabeneinbettungen aus BLSTM `blstm-crf`;
- BLSTM-CNN-CRF mit Buchstabeneinbettungen aus CNN `cnn-crf`.

## Training

- [BLSTM-CNN-CRF](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf) von UKPLab installieren;
- `blstm.py` zum Ordner `emnlp2017-bilstm-cnn-crf/` kopieren, ein Modell wählen und ausführen:
```
python blstm.py modelName trainPath devPath testPath
```
- Modelle werden in `models/` gespeichert.

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
