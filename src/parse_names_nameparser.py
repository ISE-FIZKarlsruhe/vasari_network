import csv
import re
import json
from nameparser import HumanName
from Levenshtein import distance

names_data=list()
with open('../data/indices/index_names_vol_1.json', "r", encoding="utf-8") as f:
    file_data=json.load(f)


for artist, pages in file_data.items():
    row = {"id":artist}
    row["middle_name"]=''
    name=row["id"]
    hbracket1=name.find('(')
    hbracket2=name.find(')')
            
    komma=name[:hbracket1].find(', ')
            
    #delete Title, because nameparser doesnt recognize it
    if hbracket1==-1:
        title=re.search('Fra|Don|Maestro',name)
        if re.search('Fran',name)!=None or (re.search('Dona',name)!=None):
            title=None
        if title!=None:
            name=name.replace(row["id"][title.start():title.end()+1],'')
            if (komma!=-1)&(name[komma:]==', '):
                name=name.replace(', ','')       
    else:
        title=re.search('Fra|Don|Maestro',name[:hbracket1])
        if (re.search('Fran',name)!=None) or (re.search('Dona',name)!=None):
            title=None
        if title!=None:
            name=name[:hbracket1].replace(row["id"][title.start():title.end()+1],'')+name[hbracket1:hbracket2+1]
            if (komma!=-1)&(name[komma:].find(', (')!=-1):
                name=name.replace(',','')

            

    parsed_name=HumanName(name)
    row["first_name"]=parsed_name.first
    row["surname"]=parsed_name.last
            
    #check if middle belongs to last name
    if parsed_name.middle!='':
        particle=re.search('di|da|della', parsed_name.middle)
        if particle==None:
            row["middle_name"]=parsed_name.middle
        else:
            row["surname"]=parsed_name.middle[particle.start():]+' '+row["surname"]
            if particle.start()!=0:
                row["middle_name"]=parsed_name.middle[:particle.start()-1]

                
    #full name
    if row["surname"]=='':
        row["full_name"]=row["first_name"]
    elif row["first_name"]=='':
        row["first_name"]=row["surname"]
        row["surname"]=''
        row["full_name"]=row["first_name"]
    elif row["middle_name"]!='':
        row["full_name"]=row["first_name"]+' '+row["middle_name"]+' '+row["surname"]
    else:
        row["full_name"]=row["first_name"]+' '+row["surname"]
    if title!=None:
        row["full_name"]=str(row["id"][title.start():title.end()]+' '+row["full_name"])
            

    #alias
    alias=parsed_name.nickname
    alias=alias.replace('called ','').replace('or ','')
    prep=re.search('\A[of|della|di|da]', alias)
            
    if prep!=None:
        row["alias"]=str(row["first_name"]+' '+alias)
    else:
        row["alias"]=alias
    if len(pages)!=0:
        row["pages"]=" ".join(sorted([str(x) for x in set(pages)]))
        keys=["id", "first_name", "middle_name", "surname", "full_name", "alias", "pages"]                    
        sorted_row={key: row[key] for key in keys}
        names_data.append(sorted_row)


#remove dublicates
i=0
for name1 in names_data:
    i=i+1
    s=i
    name1_variations = [name1["full_name"]]+name1["alias"].split(", ")
    name1_variations = [name.lower() for name in name1_variations if len(name)>0]
    name1_variations = set(name1_variations)
    for name2 in names_data[i:]:
        name2_variations = [name2["full_name"]]+name2["alias"].split(", ")
        name2_variations = [name.lower() for name in name2_variations if len(name)>0]
        name2_variations = set(name2_variations)
        matches=list(set(name1_variations).intersection(name2_variations))
        if matches!=[]:

            if name1["pages"]==name2["pages"]:
                print("match: ", matches)
                print("name1: ", name1)
                print("name2: ", name2)
                names_data.pop(s)
                s=s-1
        s=s+1
    s=s+1

with open('../data/index_names_vol_1.csv', 'w', encoding="utf-8") as file:
    csv_writer=csv.DictWriter(file, fieldnames=["id","first_name", "middle_name", "surname", "full_name", "alias", "pages"])
    csv_writer.writeheader()
    csv_writer.writerows(names_data)

