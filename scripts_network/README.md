# Vasari Social Network

Scripts for generating a Social Network weighted with Pointwise Mutual Information (PMI) from *The Lives of The Artists* (1568) by Giorgio Vasari.

## Setup
This code has been tested with **Python 3.9** and the following [requirements](../requirements.txt).

In order to run our scripts, it is necessary to download the pre-processed data from *The Lives of The Artists* from [Zenodo](https://doi.org/10.5281/zenodo.8395369). This is the only data format compliant with our source code. In order to run our scripts, create a directory called `data` and put it under our `main` directory.s

## Reproducing Results

In order to reproduce our results, you should run the python files in `scripts_network` in the following order:

```
python parse_names.py
```

This scripts parse the name strings from an *Index of Names* into a tabular format which separates first name, middle name, surname and aliases. The output of this step is necessary to match page fragments from Vasari by using either first name, full name and aliases.

```
python get_references.py
```

This script uses the parsed names and a coreference resolver to identify in Vasari's text nouns and pronouns which refer to entries from the *Index of Names*. 

```
python compute_pmi.py
```

This script iterates over all the references scraped from a 10 volumes edition of Vasari and, based on the frequency of each name in the text and their number of co-occurences with other names, computes 10 different tables with Pointwise Mutual Information (PMI) values. The last table, [9.csv](results/pmi_tables/9.csv), contains values which are calculated on all 10 volumes (0 1 2 3 4 5 6 7 8 9).

To create the final network, the PMI value is used to filter out connections between names whose PMI is lower than 0.

```
python create_graphs.py
```
This scripts uses the values in the PMI tables to create a visualization in HTML of the 10 dynamic networks using [Pyvis](https://pyvis.readthedocs.io/en/latest/).

```
python compute_centralities.py
```

This script computes **degree**, **beetweenness centrality** and **eigenvector centrality** of each node, using `networkx` functions.


**NOTE:** The coreference resolver requires GPU and takes some time (approx. 15 minutes). In order to speed up the process or if GPUs are not available you can use a faster but less accurate coreference resolver with CPU.

```python
from fastcoref import FCoref

model = FCoref(device='cpu')
```


