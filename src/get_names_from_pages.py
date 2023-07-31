import csv
import re
from flair.data import Sentence
from flair.models import SequenceTagger
from tqdm import tqdm


with open("../data/index_names_vol_1.csv", "r") as f:
  names_data = csv.DictReader(f)
  names_data = list(names_data)
    
with open("../data/pages_vol_1.csv", "r") as f:
  text_data = csv.DictReader(f)
  text_data = list(text_data)
    
def match_with_regex(names_data, text_data):
  output=[]
  for one_name in names_data:
    pages=one_name["pages"].split(" ")
    name_variations = [one_name["full_name"]]+one_name["first_name"].split(" ")+[one_name["surname"]]+one_name["alias"].split(", ")
    name_variations = [name for name in name_variations if len(name)>0]
    name_variations.sort(key=lambda s: len(s), reverse=True)
    lenght = len(pages)
    for i in range(0,lenght):
      page_num = pages[i]
      paragraphs = [(row["paragraph_id"], row["text"]) for row in text_data if page_num in row["pages"].split(" ")]
      if len(paragraphs)>0:
          for i in range(len(paragraphs)):
            text_page = paragraphs[i][1]
            paragraph_id = paragraphs[i][0]
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
              liste=[paragraph_id, one_name["id"], string, pos[0], pos[1]]
              output.append(liste)
  return output


def match_with_ner(names_data, text_data):
  # load tagger
  tagger=SequenceTagger.load("flair/ner-english")
  output=[]
  pbar = tqdm(total=len(text_data))
  for paragraph in text_data:
    pages=paragraph["pages"].split(" ")
    names_on_page=[]
    for name in names_data:
      namepages=name["pages"].split(" ")
      for p in namepages:
        if p in pages:
          if (name in names_on_page)==False:
            names_on_page.append(name)
     #predict ner
    sentence=Sentence(paragraph["text"])
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
      entity_type=entity.get_label("ner").value
      if entity_type=="PER":
        for name in names_on_page:
          name_variations=[name["first_name"].lower(), name["surname"].lower(), name["full_name"].lower()]
          name_variations.extend(name["alias"].lower().split(", "))
          name_variations = [name for name in name_variations if len(name)>0]
          if entity.text.lower() in name_variations:
            output_={"paragraph_num": paragraph["paragraph_id"], "start_char": entity.start_position, "end_char": entity.end_position, "surface form": entity.text, "index_name": name["id"]}
            output.append(output_)
    pbar.update(1)
  return output  

output = match_with_ner(names_data, text_data)

# change if you use match_with_regex
index=["paragraph_num", "start_char", "end_char", "surface_form", "index_name"]
with open('../data/matched_names_vol_1.csv', 'w') as file:
    csv_writer=csv.DictWriter(file, index)
    csv_writer.writeheader()
    csv_writer.writerows(output)