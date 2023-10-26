import re
import csv
import json
from tqdm import tqdm
from nltk.tokenize import sent_tokenize
import pickle
from genre.trie import Trie, MarisaTrie
from genre.fairseq_model import mGENRE

with open("./artists_vasari.json", "r", encoding="utf-8") as f:
    names_dict = json.load(f)


with open("./GENRE/data/lang_title2wikidataID-normalized_with_redirect.pkl", "rb") as f:
    lang_title2wikidataID = pickle.load(f)

with open("./GENRE/data/titles_lang_all105_marisa_trie_with_redirect.pkl", "rb") as f2:
    trie = pickle.load(f2)
    
model = mGENRE.from_pretrained("./GENRE/models/fairseq_multilingual_entity_disambiguation").eval()



output_dict = dict()

pbar = tqdm(total=len(names_dict))
for key, values in names_dict.items():
    candidates_list = []
    name = values["full_name"]+ " ("+values["alias"]+")"
    mention ="Book: Lives of the Most Eminent Painters, Sculptors and Architects by Giorgio Vasari, Publication date: 1550, Subject: [START] "+ name +" [END]" # prompt to feed to the model
    results = model.sample(
        [mention],
        prefix_allowed_tokens_fn=lambda batch_id, sent: [
            e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
            ],
            text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
            marginalize=True,
        )
    
    result = results[0]
    candidates_ids = [candidate["texts"][0]+" ("+candidate["id"]+")" for candidate in result]
    candidates_scores= [str(candidate["score"].item()) for candidate in result]
    for _id, score in zip(candidates_ids, candidates_scores):
        candidates_list.append("; ".join([_id, score]))
    output_dict[key]=candidates_list
    pbar.update(1)


with open("./output_mgenre.json", "w", encoding="utf-8") as f:
    json.dump(output_dict, f, indent=4, ensure_ascii=False)
