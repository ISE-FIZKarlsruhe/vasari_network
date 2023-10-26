import json
import re

with open("./output_bert.json", "r", encoding="utf-8") as f1:
    bert_result = json.load(f1)

with open("./output_mgenre.json", "r", encoding="utf-8") as f2:
    mgenre_result = json.load(f2)


output_dict = dict()
for key, value in bert_result.items():
    if key not in mgenre_result.keys():
        continue
    else:
        entity_linking_result = mgenre_result[key]
        Q_IDs = [re.match(".*?\((Q.*?)\).*?", res).group(1) for res in entity_linking_result]
        matched_Q_IDs = [re.match(".*?(Q.*?)>", match).group(1) for match in value]
        if len(set(Q_IDs).intersection(matched_Q_IDs))==1:
            output_dict[key]="<http://www.wikidata.org/entity/"+list(set(Q_IDs).intersection(matched_Q_IDs))[0]+">"


visited_ids = set()
ids_to_pop = set()
for key, value in output_dict.items():
    if value in visited_ids:
        ids_to_pop.add(value)
    else:
        visited_ids.add(value)

filtered_output = dict()

for key, value in output_dict.items():
    if value in ids_to_pop:
        continue
    else:
        filtered_output[key]=value

print(len(filtered_output))

with open("./linked_artists.json", "w", encoding="utf-8") as f3:
    json.dump(filtered_output, f3, indent=4, sort_keys=True,ensure_ascii=False)
