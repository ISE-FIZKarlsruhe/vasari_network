import csv
from fastcoref import LingMessCoref
import glob
import sys
import re

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


model = LingMessCoref(device='cuda:0')


def main():
  for file_name in glob.glob("../results/indices_parsed/*.csv"):
    with open(file_name, "r") as f:
        names_data = csv.DictReader(f)
        names_data = list(names_data)
        file_num = re.match(r".*?(\d+).*?", file_name).group(1)

    with open("../data/volumes/"+file_num+".csv", "r") as f:
        text_data = csv.DictReader(f)
        text_data = list(text_data)
    
    page_numbers = [int(num) for row in text_data for num in row["pages"].split(" ")]
    max_page = max(page_numbers)
    output=[]
    for pagenumber in range(1,max_page+1):
        page_text = ""
        paragraph_numbers = []
        paragraph_len = []
        names_on_page = [name for name in names_data if str(pagenumber) in name["pages"].split(" ")]
        for row in text_data:
            if str(pagenumber)==row["pages"].split(" ")[0]:
                page_text=page_text+row["text"]
                paragraph_numbers.append(row["paragraph_id"])
                paragraph_len.append(len(row["text"]))
        preds=model.predict(texts=[page_text])
        if len(preds)>0:
            characters=preds[0].get_clusters(as_strings=False)
            clusters=preds[0].get_clusters()
            for surfaces, char_pos in zip(clusters, characters):
                references = set([surface.lower() for surface in surfaces])
                name_id = []
                max_intersection = 0
                for name in names_on_page:
                    name_var=[name["first_name"].lower(), name["surname"].lower(), name["full_name"].lower()]
                    name_var.extend(name["alias"].lower().split(", "))
                    name_var = set([name for name in name_var if len(name)>0])
                    if len(references.intersection(name_var))>0 and len(references.intersection(name_var))>=max_intersection:
                        name_id.append(name["id"])
                        max_intersection=len(references.intersection(name_var))
                if len(name_id)>0:
                    text_length = 0
                    name_id = "|".join(name_id)
                    for i in range(len(surfaces)):
                        curr_paragraph = paragraph_numbers[0]
                        for p in range(len(paragraph_len)):
                            text_length+=paragraph_len[p]
                            if text_length >= char_pos[i][0]:
                                break
                            else:
                                curr_paragraph=paragraph_numbers[p]
                        output.append([pagenumber, name_id, char_pos[i],surfaces[i],curr_paragraph])

    with open("../results/references/"+file_num+".csv", "w", encoding="utf-8") as file:
        writer=csv.writer(file, delimiter=",")
        writer.writerow(["page", "index_name", "position", "reference", "paragraph"])
        writer.writerows(output)
            
        
        
        
main()
    
















    

