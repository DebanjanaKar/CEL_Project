# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 15:13:39 2018

@author: alapan
"""
import pickle
import os
from bs4 import BeautifulSoup
#file=open('/home/alapan/work_space/november_3rd/fixed_length_input/Beng_training_and_vocab_for_argument_15_11.pkl','rb')
#train_x=pickle.load(file)
#train_y=pickle.load(file)
#test_x=pickle.load(file)
#test_y=pickle.load(file)
#vocab=pickle.load(file)
#file.close()

vocab=[]
with open('/home/cel/iit_kgp_event_extraction_model/fixed_length_input/bengali_vocab.txt') as f_voc:
	for line in f_voc:
		vocab.append(line.strip())

output_path='/home/cel/iit_kgp_event_extraction_model/input_test_files/test_file_normalized/'
#print(vocab[:10])
window_size=4
path='/home/cel/iit_kgp_event_extraction_model/bengali_data/'
fullpath=""
all_words_in_doc=[]
for index,filename  in enumerate(os.listdir(path)):
    print(index)
    fullPath = os.path.join(path, filename)
    if os.path.isfile(fullPath):
        all_words_in_doc=[]
        #f= open(fullPath,'r')
        #a=[]
        #a=f.readlines()
        #print(a)
        infile= open(fullPath) 
        contents=infile.read()
        soup=BeautifulSoup(contents,'xml')
        try:
        	event_title=soup.TITLE.get_text()
        	event_content=soup.ARTICLE.get_text()
        	doc_id=soup.DOCID.get_text()
        	time=soup.DATE.get_text()
        except AttributeError:
        	print("Attribute missing")
        infile.close()
        #a=event_title+'|'+event_content
	a=event_title+'।'+event_content
        #print(a)
        #print(a)
        test_data_x=[]
        b=a.split('।')
        for sentence in b:
            word_list=sentence.split()
            #print(word_list)
            for word in word_list:
                all_words_in_doc.append(word)
                i=0
                context_window=[]
                word_index=word_list.index(word)
                while i<9:
                    #word_index=each_sentence.index(each_word)
                    if (word_index-window_size+i) < 0 or (word_index-window_size+i) >= len(word_list):
                        #word_index=each_sentence.index(each_word)
                        #print(each_sentence[word_index-window_size+i])
                        #context_window.append(each_sentence[word_index-window_size+i])
                        context_window.append(0)
                    elif (word_index-window_size+i) >=0 and (word_index-window_size+i) < len(word_list):
                        #print(len(each_sentence))
                        #print(word_index)
                        #print(word_index-window_size+i)
                        #print(each_sentence[word_index-window_size+i])
                        #context_window.append(0)
                        try:                
                            context_window.append(vocab.index(word_list[word_index-window_size+i])+1)
                        except:
                            context_window.append(vocab.index('UNK')+1)
                            #print(context_window)
                            #k=input()
                    i+=1
                test_data_x.append(context_window)
        f_pickle=open(output_path+filename.replace('xml','pkl'),'wb')
        pickle.dump(test_data_x, f_pickle, protocol=2)
        pickle.dump(all_words_in_doc, f_pickle, protocol=2)
        f_pickle.close()

def get_doc_id():
	return(doc_id , time)
  

get_doc_id()
        
            
      
            
        
