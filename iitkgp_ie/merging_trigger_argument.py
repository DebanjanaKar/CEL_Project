# -*- coding: utf-8 -*-
import os
import re

#Chande the below folders
arg_folder = '/home/cel/iit_kgp_event_extraction_model/output/test_argument_output/'#path of the argument output folder
trigger_folder = '/home/cel/iit_kgp_event_extraction_model/output/test_trigger_output/'#path for trigger output folder 
output_folder = '/home/cel/iit_kgp_event_extraction_model/output/merge_output/'

Triggers = []
Arguments = []
i = 0
dictionary = []

def process_file(trigfile,argfile) :
    triglines = trigfile.readlines()
    lines = [i.strip() for i in triglines]
# Change the below to----------->  lines.append('dummy None')
    lines.append('dummy None')
    string = ''
    prev = 'None'
    trig_pos = []
    for i,line in enumerate(lines) :
        s = re.split(' +',line)
        word = s[0]
# Change the below to----------->  trig = s[1] 
        trig = s[1] 
        if trig != 'None' and prev == 'None':   #for first word
            string = word
            trig_pos.append(i)
        elif trig != 'None' and prev == trig :
            string = string+' ' +word
        else :            
            if prev != 'None' :
                Triggers.append(prev + ' : ' +string)
                Arguments.append([])
                dictionary.append({})
                string = ''
                
            if trig != 'None' :
                string = word
                trig_pos.append(i)
                
        prev = trig
        
    if Triggers == []:
        print("no ttriggers for file : " + trigfile.name)
        return
    
    arglines = argfile.readlines()
    lines = [i.strip() for i in arglines]
# Change the below to----------->  lines.append('dummy None')
    lines.append('dummy None')
    string = ''
    prev = 'None'
    arg_pos = None
    for i,line in enumerate(lines) :
        s = re.split(' +',line)
        word = s[0]
# Change the below to----------->  arg = s[1].split('_')[0]
        arg = s[1].split('_')[0]
        if arg != 'None' and prev == 'None':
            string = word
            arg_pos=i
        elif arg != 'None' and prev == arg :
            string = string+' ' +word
        else :
            if prev != 'None' :
                array = [abs(i-arg_pos) for i in trig_pos]
                index = array.index(min(array))
                if prev not in dictionary[index] :
                    dictionary[index][prev] = ''
                dictionary[index][prev] = dictionary[index][prev] + ('|' if dictionary[index][prev] != '' else  '' ) +string
                s= prev + ' : ' +string
                Arguments[index].append(s)
                string = ''
            if arg != 'None' :
                string = word
                arg_pos = i
                
        prev = arg

    

for filename in os.listdir(arg_folder) :
    argfilename = os.path.join(arg_folder,filename)
    trigfilename = os.path.join(trigger_folder,filename)
    trigfile = open(trigfilename,'r')
    argfile = open(argfilename,'r')
    process_file(trigfile,argfile)
    trigfile.close()
    argfile.close()
    file = open(os.path.join(output_folder,filename.replace('xml','txt')),'w')
    for i in range(len(Triggers)) :
        res = Triggers[i] + '\n'
        for j,k in dictionary[i].items() :
            res = res + j +' : ' + k +'\n'
#        res = '\n'.join(Arguments[i])
        res = res + '\n\n'
        file.write(res)
    Triggers = []
    Arguments = []
    dictionary = []
    file.close()        
