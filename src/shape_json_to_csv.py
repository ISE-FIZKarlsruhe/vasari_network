import json
import csv


with open("index_names_vol1.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
output = []
for key, value in data.items():
    output.append({
        "id":str(key),
        "first_name":"",
        "surname":"",
        "full_name":"",
        "alias":"",
        "pages":" ".join([str(page) for page in value])
    })

keyz = output[0].keys()
with open("index_names_vol1.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f,keyz)
    dict_writer.writeheader()
    dict_writer.writerows(output)