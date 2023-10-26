# Vasari Social Network

Generation of a social network from *The Lives of The Artists* (1568) by Giorgio Vasari. 

[GitHub Page](https://ise-fizkarlsruhe.github.io/vasari_network/)

## Setup
This code has been tested with **Python 3.9** and the following [requirements](requirements.txt).

In order to run our scripts, it is necessary to download the pre-processed data from *The Lives of The Artists* from [Zenodo](https://doi.org/10.5281/zenodo.8395369). This is the only data format compliant with our source code. In order to run our scripts, create a directory called `data` and put it under our `main` directory.

```
main/
    data/
    results/ 
    scripts_network/    #scripts for generating a social network
    linking_vasari_wikidata/    #scripts to link artists in the network to Wikidata
    scripts_rdf/    #scripts to convert social network into Knowledge Graph
    scripts_scraping/   #scripts to generate input data (for documentation)
    rdfs/   #turtle serialization of the Knowledge Graph
    requirements.txt
    LICENSE
    README.md
```

## Results on Zenodo

The results from this research are also stored indipenedently from this repository on [Zenodo](https://doi.org/10.5281/zenodo.8395425).

