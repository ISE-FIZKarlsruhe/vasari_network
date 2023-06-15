import csv
import json
import re
from Levenshtein import distance


def filter_candidates(item, wikidata_dict):
    candidates = []
    for candidate in item["candidates"]:
        # take the wikidata id from the string using regex
        wikidata_id = re.findall("Q\d+", candidate)[0]
        # find if class "human" is a class of the candidate
        if "http://www.wikidata.org/entity/Q5" in wikidata_dict[wikidata_id]["classes"]:
            candidates.append(candidate)
    return candidates

def compute_min_distance(item, candidates, index, wikidata_dict):
    index_name = item["index_name"]
    min_distances = []
    for row in index:
        if row["id"]==index_name:
            # create a list containing the full name and alias of the person mentioned
            name_variants = [row["full_name"]] + [row["alias"].lower()]
    for candidate in candidates:
        # get the labels of the filtered candidates and compute distance between wikidata labels and variants in index
        lev_distances = []
        wikidata_id = re.findall("Q\d+", candidate)[0]
        labels = wikidata_dict[wikidata_id]["labels"]
        for variant in name_variants:
            for label in labels:
                # compute levenshtein distance between labels and variants, use .lower() to ignore casing
                lev_distance = distance(variant.lower(), label.lower())
                lev_distances.append(lev_distance)
        #get the min distance for each candidate
        min_distance = min(lev_distances)
        min_distances.append(min_distance)
    return min_distances


with open("../data/index_names_vol_1.csv", "r", encoding="utf-8") as f1:
    index = csv.DictReader(f1)
    index = list(index)

with open("../nel/200_candidates.json", "r", encoding="utf-8") as f2:
    list_of_items = json.load(f2)

with open("../nel/wikidata_dict_200_candidates.json", "r", encoding="utf-8") as f3:
    wikidata_dict = json.load(f3)


example = list_of_items[0]
filtered_candidates = filter_candidates(item=example, wikidata_dict=wikidata_dict)
print(filtered_candidates)
min_distances = compute_min_distance(item=example, candidates=filtered_candidates, wikidata_dict=wikidata_dict, index=index)

output = {
    "page":example["page"],
    "start_pos":example["start_pos"],
    "end_pos":example["end_pos"],
    "surface":example["surface"],
    "index_name":example["index_name"],
    "candidates":filtered_candidates,
    "distances":min_distances
}
print(output)

with open("../nel/sample_levenshtein_distances.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

output=[]
for item_ in list_of_items:
  filtered_candidates= filter_candidates(item=item_, wikidata_dict=wikidata_dict)
  
  min_distances = compute_min_distance(item=item_, candidates=filtered_candidates, wikidata_dict=wikidata_dict, index=index)
  output_={
      "page":item_["page"],
      "start_pos":item_["start_pos"],
      "end_pos":item_["end_pos"],
      "surface":item_["surface"],
      "index_name":item_["index_name"],
      "candidates":filtered_candidates,
      "distances":min_distances
  }
  output.append(output_)

print(output)

with open("../nel/levenshtein_distances.json", "w", encoding="utf-8") as f4:
    json.dump(output, f4, ensure_ascii=False, indent=4)
