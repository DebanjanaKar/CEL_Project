
# coding: utf-8

# In[3]:

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
import os
import real_test_file_preprocessing as rtf
import bangla_date_resolve as bdr
from shared_ie import lat_long
import time

import mysql.connector

database_conn = mysql.connector.connect(
  host = "localhost.localdomain",
#  proxy = "http://172.16.2.30/",
  user = "root",
  password = "Cel_123!",
  database='cel'
)

cursor_conn = database_conn.cursor()
path='/home/cel/iit_kgp_event_extraction_model/output/merge_output/'
#output_path='/home/cel/iit_kgp_event_extraction_model/output/merge_output_tabular/'
xml_path='/home/cel/crawlers/datasets/merge/'

import mysql.connector

mydb = mysql.connector.connect(
  host = "localhost.localdomain",
#  proxy = "http://172.16.2.30/",
  user = "root",
  password = "Cel_123!",
  database='cel'
)

for filename  in os.listdir(path):
    fullPath = os.path.join(path, filename)
    print(fullPath)
    if os.path.isfile(fullPath):
        list_row=[]
        key_term=['DOCID','EVENT_TYPE','LAT_LONG','DOC_TIME','DOC_DATE','DOC_PATH','TIME-ARG', 'PLACE-ARG', 'REASON-ARG','AFTER','CASUALTIES-ARG','PARTICIPANT-ARG','MAGNITUDE-ARG','EPICENTRE-ARG','TYPE-ARG','TEMPERATURE-ARG','SPEED-ARG','INTENSITY-ARG','DEPTH-ARG','NAME-ARG','DISPLAY']
        row = dict.fromkeys(key_term,'NULL')
        with open (fullPath) as f1:
            f=1 #checking first line in the file
            b=1 #as it is first line so no previous line
            flag = 0
            for line in f1:
                #print(line)
                a=line.split(':')
                #print(a)
                #k=input()
                if len(a)<2:
                    
               	    if flag==0:
                      #flag=1
                      lat,longi=lat_long.loc_resolve("")
                      lat_longit = str(lat)+'|'+str(longi)
                      row['LAT_LONG']=lat_longit
                      flag=1
                    else:
                    	flag=1
                    
                    b=1
                    continue
                    
                    #list_row.append(row)
                    
                if f==1 or b==1: #checking if (first line) or (previous line blank)
                    
                    f=0 #we have already processed first line
                    b=0 #as we processing first line, for next line 'b' flag is 0 i.e. previous line is not blank
                    #that means it is a line with event type and corresponding trigger word	
                    list_row.append(row)#it should only be executed when (b==1 and f!=1); so some modification have to be done here 
                    flag=0
                    row = dict.fromkeys(key_term,'--')
                    a=line.split(':')
                    try:
                        row['event_type']=a[0].strip()
                        #row['event_trigger']=a[1].strip()
                        row['LANGUAGE']="bn"
                        doc_id,time_1=rtf.get_doc_id()
                        t=bdr.resolve_date(time_1)
                        row['DOCID']=doc_id
                        row['DOC_DATE']=t[0]
                        row['DOC_TIME']=t[1]
                        row['DOC_PATH']=xml_path
                        row['DISPLAY']="no"
                    except:
                        print(line)
                    #print(row)
                    continue
                if f==0 and b==0:#checking if it is not first line and previous line is not blank			
                    f=0#it is not first line
                    b=0# for next line previous lineis not blank

                    a=line.split(':')
                    
                    if(str(a[0].strip())=="PLACE-ARG"):
                      lat,longi=lat_long.loc_resolve(str(a[1].strip()))
                      #time.sleep(5) 
                      lat_longit = str(lat)+'|'+str(longi)
                      row['LAT_LONG']=lat_longit
                      flag=1

                    
                    try: 
                        row[a[0].strip()]=a[1].strip()
                    except:
                        print(line)
                    
                    print('---------------------------------------------------------')
                    if row['LAT_LONG']=='--':
                      row['LAT_LONG']=""
                    if (all(value == "NULL" for value in row.values())==False and row['EVENT_TYPE']!='--'):
                      print(row)
                      for index,i in enumerate(row):
                          if(i=='--'):
                              row[index]=""
                      query = "INSERT INTO master_table (DOCID,EVENT_TYPE,LANGUAGE,DOC_DATE,DOC_TIME,DOC_PATH,TIME_ARG,PLACE_ARG,REASON_ARG, CASUALTIES_ARG,TYPE_ARG,PARTICIPANT_ARG,INTENSITY_ARG,MAGNITUDE_ARG, NAME_ARG,SPEED_ARG,DEPTH_ARG,AFTER_EFFECTS_ARG,TEMPERATURE_ARG,EPICENTRE_ARG,LAT_LONG,DISPLAY) VALUES ('"+row['DOCID']+"','"+row['EVENT_TYPE']+"','"+row['LANGUAGE']+"','"+row['DOC_DATE']+"','"+row['DOC_TIME']+"','"+row['DOC_PATH']+"','"+row['TIME-ARG']+"','"+row['PLACE-ARG']+"','"+row['REASON-ARG']+"','"+row['CASUALTIES-ARG']+"','"+row['TYPE-ARG']+"','"+row['PARTICIPANT-ARG']+"','"+row['INTENSITY-ARG']+"','"+row['MAGNITUDE-ARG']+"','"+row['NAME-ARG']+"','"+row['SPEED-ARG']+"','"+row['DEPTH-ARG']+"','"+row['AFTER']+"','"+row['TEMPERATURE-ARG']+"','"+row['EPICENTRE-ARG']+"','"+row['LAT_LONG']+"','"+row['DISPLAY']+"');"
                      print(query)
                      cursor_conn.execute(query)
                      database_conn.commit()
                    print('---------------------------------------------------------')
                    continue
                    #print(row)
                        #continue
                    
          
            
            list_row.append(row)
            
            
            #df = pd.DataFrame(list_row)

            #df1=df.reindex(columns=['DOCID','EVENT_TYPE','LANGUAGE','DOC_DATE','DOC_TIME','DOC_PATH', 'TIME_ARG', 'PLACE_ARG', 'REASON_ARG','AFTER_EFFECTS_ARG','CASUALTIES_ARG','PARTICIPANT_ARG','MAGNITUDE_ARG','EPICENTRE_ARG','TYPE_ARG','TEMPERATURE_ARG','SPEED_ARG','INTENSITY_ARG','DEPTH-ARG','NAME-ARG','LAT_LONG','DISPLAY'])
			
			
            #df1.to_csv(output_path+filename.replace('.txt','.csv'), sep='\t', encoding='utf-8', index=False,  tupleize_cols=True)
	

