import requests
import csv, json
import random
import re
import time
from tqdm import tqdm

def get_data_from_kb(_id):
    url = "https://query.wikidata.org/sparql"
    headers = {'User-Agent': 'New research project for art history'}
    labels = []
    classes = []
    query = """PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?alias ?class WHERE {wd:"""+\
    _id+ """ (wdt:P735|wdt:P734)?/(wdt:P1813|wdt:P1705|wdt:P1559|wdt:P1477|wdt:P1449|wdt:P742|skos:altLabel|rdfs:label) ?alias ;
    wdt:P31 ?class;
    FILTER(LANGMATCHES(LANG(?alias), "en") || LANGMATCHES(LANG(?alias), "it"))
    }"""
    r = requests.get(url, params = {'format': 'json', 'query': query}, headers=headers)
    results = r.json()
    for result in results["results"]["bindings"]:
        label = result["alias"]["value"]
        _class = result["class"]["value"]
        labels.append(label)
        classes.append(_class)
    return labels, classes

with open("../data/sample_200.csv", "r", encoding="utf-8") as f:
    sample = list(csv.DictReader(f))

wikidata_dict = dict()
pbar=tqdm(total=len(sample))
for row in sample:
    try:
        ids = re.findall("(?<=\()Q\d+", row["candidates"])
        for _id in ids:
            if _id not in wikidata_dict.keys():
                time.sleep(20)
                labels, classes = get_data_from_kb(_id)
                wikidata_dict[_id]={"labels":labels, "classes":classes}
        pbar.update(1)
    except Exception as e:
        print(e)
        break

with open("../data/wikidata_dict.json", "w") as fp:
    json.dump(wikidata_dict, fp, indent=4)

