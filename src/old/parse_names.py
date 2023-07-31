import csv
import re
output=list()
with open('index_names_vol_1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count==0:
            index=row
        if (row!=[])& (line_count!=0):
            
            name=row[0]
            hbracket1=name.find('(')
            hbracket2=name.find(')')
            
            komma=name[:hbracket1].find(', ')
            
            if hbracket1==-1:
                whitespace=name.rfind(' ')
                particle=re.search(' di| da| della', name)
                title=re.search('Fra|Don|Maestro',name)
                if re.search('Fran',name)!=None or (re.search('Dona',name)!=None):
                    title=None
                
                    
            else:
                whitespace=name[:hbracket1-1].rfind(' ')
                particle=re.search(' di| da| della| the', name[:hbracket1])
                title=re.search('Fra|Don|Maestro',name[:hbracket1])
                if (re.search('Fran',name)!=None) or (re.search('Dona',name)!=None):
                    title=None
            if title!=None:
                name=name.replace(row[0][title.start():title.end()+1],'')
                if (komma!=-1)&(name[komma:]==', '):
                    name=name.replace(', ','')
                if (komma!=-1)&(name[komma:].find(', (')!=-1):
                    name=name.replace(',','')

            bracket1=name.find('(')
            bracket2=name.find(')')
            
            komma=name[:bracket1].find(', ')
            
            if bracket1==-1:
                whitespace=name.rfind(' ')
                particle=re.search(' di| da| della', name)
                              
                    
            else:
                whitespace=name[:bracket1-1].rfind(' ')
                particle=re.search(' di| da| della| the', name[:bracket1])

            print(row[0])
            print(name)
            print(komma)
            if (komma==-1):
                if whitespace==-1:
                    if bracket1==-1:
                        row[1]=name #only first name
                        row[3]=name

                    else:
                        row[1]=name[:bracket1-1]
                        row[3]=name[:bracket1-1]
                                                                 
                else:
                    
                    if (particle==None) & (bracket1==-1):
                        row[1]=name[0:whitespace] #first name, normal version
                        row[2]=name[whitespace+1:] #last name, normal version
                        row[3]=row[0]
                    elif (particle==None) & (bracket1!=-1):
                        row[1]=name[:whitespace] #first name, normal version
                        row[2]=name[whitespace+1:bracket1-1] #last name with alias
                        row[3]=row[0][:hbracket1-1]
                        
                    elif (particle!=None) & (bracket1==-1):
                        row[1]=name[:particle.start()]
                        row[2]=name[particle.start()+1:]
                        row[3]=row[0]
                        if title!=None:
                            row[3]=str(row[0][title.start():title.end()]+' '+name)
                    elif (particle!=None) & (bracket1!=-1):
                        row[1]=name[:particle.start()]
                        row[2]=name[particle.start()+1:bracket1-1]
                        row[3]=row[0][:hbracket1-1]
                        
                            
                    
            else:
                if particle==None:
                    row[2]=name[:komma]
                    if (bracket1==-1):
                        row[1]=name[komma+2:]
                    
                    if (bracket1!=-1):
                        row[1]=name[komma+2:bracket1-1]
                    
                if particle!=None:
                    row[1]=name[komma+2:particle.start()]
                    row[2]=str(name[particle.start()+1:particle.end()]+" "+name[:komma])
                    if (name[particle.end():]!='') & (name[particle.end():].find(' (')==-1):
                        row[2]=str(name[particle.start()+1:]+" "+name[:komma])
                if title==None:
                    row[3]=str(row[1]+' '+row[2])
                if (title!=None):
                    row[3]=str(row[0][title.start():title.end()]+' '+row[1]+' '+row[2])

#alias
            if bracket1!=-1:
                        alias=row[0][hbracket1+1:hbracket2].replace('called ','').replace('or ', '')
                        prep=re.search('\A[of|della|di|da]', alias)
            
                        if prep!=None :
                            row[4]=str(row[1]+' '+alias)
                        else:
                            row[4]=alias
                        
            print(row)
            output.append(row)
        line_count=+1
print(output)
with open('index_names_vol_1.csv', 'w') as file:
    csv_writer=csv.writer(file)
    csv_writer.writerow(index)
    csv_writer.writerows(output)
