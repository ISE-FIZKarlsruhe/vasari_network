import json
from tqdm import tqdm
import re
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv

with open("./artists_vasari.json", "r", encoding="utf-8") as f:
    names_dict = json.load(f)

names_variants = dict()
for key, value in names_dict.items():
    names_variants[key]=[value["full_name"]]+ value["alias"].split(", ")


tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model = BertModel.from_pretrained("bert-base-multilingual-cased")

with open("./artists_before_1568.csv", "r", encoding="utf-8") as f:
    wikidata_artists = csv.DictReader(f)
    wikidata_artists = list(wikidata_artists)

wikidata_names = dict()
for row in wikidata_artists:
    if row["o"].endswith('"@en') and not row["p"].endswith("description>"):
        name_variant = re.match('\"(.*?)\"@en', row["o"].encode('utf-8').decode('unicode-escape')).group(1)
        if row["s"] in wikidata_names.keys():
            wikidata_names[row["s"]].add(name_variant)
        else:
            wikidata_names[row["s"]]=set([name_variant])
        
result = dict()

def get_wordvectors(nameslist):
    #create file of wordvectors for full_name and alias
    names_vectors=[]
    for name in nameslist:
        if name=="":
            names_vectors.append(np.zeros(768)) #if name has no alias, set wordvector to zero
        else:
            inputs=tokenizer(name, return_tensors="pt")
            outputs = model(**inputs) #create vectors
            last_hidden_states = outputs.last_hidden_state
            vector=last_hidden_states[0].detach().numpy() #use only the last hidden state
            length=len(vector)-2 #first and last vectors are from tokens
            fullname_vector=np.zeros(768)
            #average vectors
            for i in range(1,length+1,1):
                fullname_vector+=vector[i]
            fullname_vector/=length
            names_vectors.append(fullname_vector)
    return names_vectors

wikidata_vectors = dict()

pbar = tqdm(total=len(wikidata_names.keys()))
for wiki_id, labels in wikidata_names.items():
    wiki_names_vectors = get_wordvectors(labels)    
    wikidata_vectors[wiki_id]=wiki_names_vectors
    pbar.update(1)
pbar.close()

pbar = tqdm(total=len(names_dict.keys()))
for _id, variants in names_variants.items():
    vasari_names_vectors = get_wordvectors(variants)
    for wiki_id, wiki_names_vectors in wikidata_vectors.items():
        labels_similarity = cosine_similarity(vasari_names_vectors, wiki_names_vectors)
        similarities = []
        for i in range(len(variants)):
            for j in range(len(wiki_names_vectors)):
                similarities.append(labels_similarity[i,j])
        if max(similarities)>0.95:
            if _id in result.keys():
                result[_id].add(wiki_id)
            else:
                result[_id]=set([wiki_id])
    pbar.update(1)

total = 0
count = 0
for _id in result.keys():
    result[_id]= list(result[_id])
    if len(result[_id])==1:
        count+=1
    total+=1


print("Total artists: "+ str(len(result.keys())))
print("Matched artists" + str(count))

with open("./output_bert.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)


