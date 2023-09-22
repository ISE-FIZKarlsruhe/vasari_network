import csv
from fastcoref import FCoref

model = FCoref(device='cuda:0')

with open(".../data/index_names_vol_1.csv", "r") as f:
  names_data = csv.DictReader(f)
  names_data = list(names_data)
with open(".../data/pages_vol_1.csv", "r") as f:
  text_data = csv.DictReader(f)
  text_data = list(text_data)

  output=[]
all_paragraphs=[]
for pagenumber in range(1,225):
  pagetext=""
  paragraph_num=[]
  paragraph_length=[]
  for paragraph in text_data:
    pages_of_para=paragraph["pages"].split(" ")

    if str(pagenumber) in pages_of_para:
      #concatenate paragraphs, that are on the same page
      pagetext=pagetext+paragraph["text"]
      #save paragraph numbers and lenght of paragraph
      paragraph_num.append(paragraph["paragraph_id"])
      paragraph_length.append(len(paragraph["text"]))
  
  #predict coref
  preds=model.predict(texts=[pagetext])
  characters=preds[0].get_clusters(as_strings=False)
  clusters=preds[0].get_clusters()
  print(clusters)
  for i, cluster in enumerate(clusters):
    cluster_linked=False
    for reference in cluster:
      for name in names_data:
        name_var=[name["first_name"].lower(), name["surname"].lower(), name["full_name"].lower()]
        name_var.extend(name["alias"].lower().split(", "))
        name_var = [name for name in name_var if len(name)>0]
        #link culster to name in index_names
        if reference.lower() in name_var:
          
          for k in range(len(cluster)):
            data=[pagenumber, name["id"], characters[i][k], cluster[k]]
            output.append(data)
          cluster_linked=True
          break #only link once
      if reference.lower() in name_var:
        break #only link once
    

    paragraphs_of_cluster=[]
    
    if cluster_linked==True:
      #get paragraphs of each mention
      for character in characters[i]:
        text_length=0
        for p in range(len(paragraph_num)):
          text_length=text_length+paragraph_length[p]
          if text_length>(character[0]+1):
            paragraphs_of_cluster.append(paragraph_num[p])
            break
      
      all_paragraphs.extend(paragraphs_of_cluster)
for n in range(len(all_paragraphs)):
  output[n].append(all_paragraphs[n])    
        
with open(".../data/coref_multiple_paragraphs.csv", "w") as file:
  writer=csv.writer(file, delimiter=",")
  writer.writerow(["page", "index_name", "position", "reference", "paragraph"])
  writer.writerows(output)