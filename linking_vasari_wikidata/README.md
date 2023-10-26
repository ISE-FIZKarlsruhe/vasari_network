# Linking Artists Referenced By Vasari to Wikidata

This repository contains data and source code used to link the artists mentioned in the Index of Names of Giorgio Vasari's *Lives of The Artists* to Wikidata using BERT and Entity Linking.

## Requirements

This code has been tested with **Python 3.9** and the following [requirements](requirements.txt).


The Entity Linking script `run_mgenre.py` relies on the [mGENRE](https://github.com/facebookresearch/GENRE) model from Facebook. To run these scripts, you should install the **GENRE** library from source.

```
git clone https://github.com/facebookresearch/GENRE.git 
cd GENRE
pip install --editable ./
```

Moreover, for running the mGENRE model you need to download [fairseq_multilingual_entity_disambiguation](https://dl.fbaipublicfiles.com/GENRE/fairseq_multilingual_entity_disambiguation.tar.gz), [titles_lang_all105_trie_with_redirect.pkl](http://dl.fbaipublicfiles.com/GENRE/titles_lang_all105_trie_with_redirect.pkl) and [lang_title2wikidataID-normalized_with_redirect](https://dl.fbaipublicfiles.com/GENRE/lang_title2wikidataID-normalized_with_redirect.pkl).

## Reproducing Results

In order to reproduce our results, you should run the python files in `linking_vasari_wikidata` in the following order:

```
python run_bert.py
```

This script generates, for each entry in the Index of Names of Giorgio Vasari, a list of potential candidates for Entity Linking in Wikidata by using the similarity between full names and nicknames used by Vasari and the labels of an entity in Wikidata. The candidates are generated from `artists_before_1568.csv`, a dump of Wikidata with artists born before or during 1568 (year of publication of Vasari's book) and by applying a minimum threshold of 0.95 for string similarity.

```
python run_mgenre.py
```

This script uses the mGENRE model from Facebook to generate a set of Wikidata IDs out of each artist name. The Entity Linker works by taking as input a textual reference in context, e.g. *Book: The Lives of The Artists by Giorgio Vasari, Publication Date: 1568, Subject: {ArtistName}* to return a set of Wikidata entities.

```
python merge_results.py
```

This script intersects the output of BERT with the output of mGENRE to find the best candidate in Wikidata to disambiguate a name. Only names which have a unique candidate in the intersection of the results and whose Wikidata entity does not appear as candidate for any other artist are saved in the result `linked_artists.csv`.