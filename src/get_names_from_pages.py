import csv
import re

with open("../data/index_names_vol_1.csv", "r") as f:
  names_data = csv.DictReader(f)
  names_data = list(names_data)
    
with open("../data/pages_vol_1.csv", "r") as f:
  text_data = csv.DictReader(f)
  text_data = list(text_data)
    
    
output=[]
for one_name in names_data:
  pages=one_name["pages"].split(" ")
  name_variations = [one_name["full_name"]]+[one_name["first_name"]]+[one_name["surname"]]+one_name["alias"].split(", ")
  name_variations = [name for name in name_variations if len(name)>0]
  lenght = len(pages)
  for i in range(0,lenght):
    page_num = pages[i]
    text_page = [row["text"] for row in text_data if row["pg_num"]==page_num]
    if len(text_page)>0:
        text_page = text_page[0]
        re_matches = list()
        matched_chars = set()
        for name in name_variations:
            matches = re.finditer(name, text_page, re.IGNORECASE) 
            matches = [(m.start(0), m.end(0)) for m in matches]
            for m in matches:
                range_chars = set(range(m[0], m[1]))
                if len(matched_chars.intersection(range_chars))==0:
                    re_matches.append(m)
                    matched_chars.update(range_chars)
                else:
                    continue
        pg_strings = [text_page[re_match[0]:re_match[1]] for re_match in re_matches]
        for pos, string in zip(re_matches, pg_strings):
          liste=[page_num, one_name["id"], string, pos[0], pos[1]]
          output.append(liste)
        
index=["page_number", "id", "match_string", "start_pos", "end_pos"]
with open('../data/pages_names.csv', 'w') as file:
    csv_writer=csv.writer(file)
    csv_writer.writerow(index)
    csv_writer.writerows(output)