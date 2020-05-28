
# coding: utf-8

# In[3]:


import pandas as pd
import os

path='/home/cel/iit_kgp_event_extraction_model/output/merge_output'
output_path='../work_space/november/beng_event_extract/merged_tabular_21_12/'

for filename  in os.listdir(path):
    file_name="bn.2018-12-22.9.txt"
    fullPath = os.path.join(path, filename)
    if os.path.isfile(fullPath):
        list_row=[]
        key_term=['event_id','event_type','event_trigger','TIME-ARG', 'PLACE-ARG', 'REASON-ARG','AFTER','CASUALTIES-ARG','PARTICIPANT-ARG','MAGNITUDE-ARG','EPICENTRE-ARG','TYPE-ARG','TEMPERATURE-ARG','SPEED-ARG','INTENSITY-ARG','DEPTH-ARG','NAME-ARG']
        row = dict.fromkeys(key_term,'--')
        with open (fullPath) as f1:
            f=1 #checking first line in the file
            b=1 #as it is first line so no previous line
            for line in f1:
                #print(line)
                a=line.split(':')
                #print(a)
                #k=input()
                if len(a)<2:
                    b=1
                    #list_row.append(row)
                    continue
                if f==1 or b==1: #checking if (first line) or (previous line blank)
                    f=0 #we have already processed first line
                    b=0 #as we processing first line, for next line 'b' flag is 0 i.e. previous line is not blank
                    #that means it is a line with event type and corresponding trigger word
                    list_row.append(row)#it should only be executed when (b==1 and f!=1); so some modification have to be done here 
                    row = dict.fromkeys(key_term,'--')
                    a=line.split(':')
                    try:
                        row['event_type']=a[0].strip()
                        row['event_trigger']=a[1].strip()
                    except:
                        print(line)
                    #print(row)
                    continue
                if f==0 and b==0:#checking if it is not first line and previous line is not blank
                    f=0#it is not first line
                    b=0# for next line previous lineis not blank
                    a=line.split(':')
                    try: 
                        row[a[0].strip()]=a[1].strip()
                    except:
                        print(line)
                        #continue
                    #print(row)
                    continue
            
            list_row.append(row)

            df = pd.DataFrame(list_row)

            df1=df.reindex(columns=['event_id','event_type','event_trigger','TIME-ARG', 'PLACE-ARG', 'REASON-ARG','AFTER','CASUALTIES-ARG','PARTICIPANT-ARG','MAGNITUDE-ARG','EPICENTRE-ARG','TYPE-ARG','TEMPERATURE-ARG','SPEED-ARG','INTENSITY-ARG','DEPTH-ARG','NAME-ARG'])
            print('---------------------------')
            print(filename)
            print(df1)
            print('---------------------------')
            
            #df1.to_csv(output_path+filename.replace('.txt','.csv'), sep='\t', encoding='utf-8', index=False)
            #f1.close()
    break        

