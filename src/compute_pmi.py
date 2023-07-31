import csv
import math

with open("../data/matched_names_vol_1.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f)
    data = list(data)

paragraphs_set = set([row["paragraph_id"] for row in data])


name_paragraph_dict = dict()
for paragraph in paragraphs_set:
    names = set([row["name"] for row in data if row["paragraph_id"]==paragraph])
    for name in names:
        if name in name_paragraph_dict.keys():
            name_paragraph_dict[name]+=1
        else:
            name_paragraph_dict[name]=1

probability_dict = dict()
for name in name_paragraph_dict.keys():
    probability_dict[name]=name_paragraph_dict[name]/len(paragraphs_set)

cooccurence_list = list()

for paragraph in paragraphs_set:
    names = set()
    for row in data:
        if row["paragraph_id"]==paragraph:
            names.add(row["name"])
    for name1 in names:
        for name2 in names:
            if name2!=name1:
                cooccurence_list.append((name1, name2))


output = []
for name1 in probability_dict.keys():
    cooccurence_dict = dict()
    for cooccurence in cooccurence_list:
        if cooccurence[0]==name1:
            if cooccurence[1] in cooccurence_dict.keys():
                cooccurence_dict[cooccurence[1]]+=1
            else:
                cooccurence_dict[cooccurence[1]]=1
    for name2 in cooccurence_dict.keys():
        p_x = probability_dict[name1]
        p_y = probability_dict[name2]
        p_yx = (cooccurence_dict[name2]/len(paragraphs_set))/probability_dict[name1]
        pmi_yx = math.log(p_yx/p_y, 2)

        output.append({"x":name1, "p_x":p_x, "y":name2, "p_y":p_y, "p_yx":p_yx, "pmi_yx":pmi_yx})


sorted_output = sorted(output, key=lambda item: float(item["pmi_yx"]), reverse=True)
computed_pairs = set()
new_output = []
for x in sorted_output:
    if (x["y"], x["x"]) in computed_pairs:
        continue
    else:
        new_output.append(x)
        computed_pairs.add((x["x"], x["y"]))

with open("../data/pmi_table.csv", "w", encoding="utf-8") as out_f:
    csv_writer = csv.DictWriter(out_f, new_output[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(new_output)