import pandas as pd
import nltk
import string
import re
import pickle
from glob import glob
import codecs
from bs4 import BeautifulSoup
import numpy as np
from create_annotated_file import get_word_appended
import sys
import os
sys.version
import argparse
parser = argparse.ArgumentParser(description='trigger detection classification and argument extraction')

parser.add_argument('--doc', default="", type=str, metavar='N', help='file to extract information')
parser.add_argument('--frame', default="4359c55cdb1dffea1d411e7fb0a2c3f1", type=str, metavar='N', help='frame name')
parser.add_argument('--dt', default="", type=str, metavar='N', help='date')
parser.add_argument('--tm', default="", type=str, metavar='N', help='time')
parser.add_argument('--docpath', default="../../outside_data/", type=str, metavar='N', help='doc path')
parser.add_argument('--disp', default="no", type=str, metavar='N', help='no for testing yes for real')
parser.add_argument('--lang', default="hi", type=str, metavar='N', help='language')

import json

args = parser.parse_args()



text_file= ""
with codecs.open(args.doc, encoding='utf-8') as file:
	text_file = file.read()

#print(text_file)

def clean(token):
	token=token.replace('।','')
#	token=token.replace('।','\n')
	token=token.replace('?','')
	token=token.replace(',','')
	token=token.replace('!','')
	token=token.replace('"','')
	token=token.replace("”",'')
	token=token.replace(":",'')
	token=token.replace(";",'')
	token=token.replace(" ",'')
	token=token.replace('|','')
	return token



def doc2sent(s):
	sent=[]
	s1=[]
	flag=0
	for i in range(len(s)):
		if  '?' in s[i] or '!' in s[i] or '।' in s[i] or '.' in s[i][-2:-1]:
			s1.append(clean(s[i]))
			sent.append(s1)
			s1=[]
			flag=1
		else:
			s1.append(clean(s[i]))
			flag=0
	if flag==0:
		sent.append(s1)
	return sent



sentences=doc2sent(text_file.split())
#print(sentences)
#print(sentences)



#print("loading dictionaries...")
sequence_length = 75
class_index = json.load(open("../data/dictionaries/class_index.json"))
arg_index = json.load(open("../data/dictionaries/arg_index.json"))
word_index = pd.read_pickle("../data/dictionaries/universal_word_index.pickle")
lang = args.lang

#print(word_index[(sentences[0][0],lang)])
#print("done...")

#####code for padding####

def pad_s(l,dim,val):
	if len(l)>dim:
		return l[:dim]
	else:
		return l+[val]*(dim-len(l))

pad, _ = word_index[('pad','p')]
#print("pad-->",pad)

########################
#print("pading sentences...")
sentences = [pad_s(i, sequence_length, 'pad') for i in sentences]
#print(sentences)
#print(sentences)

print("indexing words...")
indexed = []
for i in sentences:
	ind = []
	for j in i:
		try:
			z,f = word_index[(j,lang)]
			ind.append(z)
		except:
			ind.append(76171)
	indexed.append(ind)

# print(indexed)

inv_class = {v: k for k, v in class_index.items()}
inv_arg = {v: k for k, v in arg_index.items()}
inv_word = {v: k for k, v in word_index.items()}

label_size=len(class_index)+1

from keras import callbacks
from keras.models import Sequential,Model
from keras.layers import *
from keras.layers.wrappers import Bidirectional
from keras.initializers import RandomUniform,Zeros
from keras import regularizers
from keras.layers import Input, RepeatVector, concatenate, Activation, Permute, merge

#logging.basicConfig(level=logging.DEBUG)
from keras.models import load_model as ld
from keras.layers import Embedding

indexed = np.asarray(indexed)
indexed = indexed.reshape(indexed.shape[0],indexed.shape[1],1)

path_class = "../models/3_l_c_default_lang_"+args.lang+".hdf5"
path_arg = '../models/3_l_arg_default_lang_'+args.lang+'.hdf5'
model_class = ld(path_class)
model_arg = ld(path_arg)

class_predict = model_class.predict(indexed)

# trig_predict = np.argmax(trig_predict.reshape(len(trig_predict)*sequence_length,2),axis=-1)
class_predict = np.argmax(class_predict.reshape(len(class_predict)*sequence_length,label_size),axis=-1)
trig_predict = list(class_predict)
class_predict = list(set(class_predict))
class_predict.remove(1)
class_predict = [inv_class[i] for i in class_predict]
print(class_predict)
#print("triggers", trig_predict)
#print("EVENTS", class_predict)

indexed = indexed.reshape(indexed.shape[0],indexed.shape[1])

#print(indexed)
index = []
for i in indexed:
	ind = []
	for j in i:
		if j == 76171:
			ind.append(1)
		else:
			ind.append(j)
	index.append(ind)
index = np.asarray(index)
#print(index)
#arg_predict = list(model_arg.predict(indexed))
arg_predict = list(model_arg.predict(index))
arguments = [i for i,_ in arg_index.items() if i!='P']

d = pd.DataFrame(columns = ['event','words','real_words'])
#d = pd.DataFrame(columns = ['words'])
trig_pred = []
for i in trig_predict:
	if i == 1:
		trig_pred.append(0)
	else:
		trig_pred.append(1)

d['event'] = [inv_class[i] for i in trig_predict]
#print("trig_pred-->",len(trig_pred))
indexed = indexed.reshape(indexed.shape[0]*indexed.shape[1])
#print("indexed-->", len(indexed))
d['words'] = list(indexed)
d['real_words'] = [j for i in sentences for j in i]
for i,j in zip(arg_predict,arguments):
	i=i.reshape(len(i)*sequence_length,2)
	i=np.asarray(i.argmax(axis=-1))
	d[j] = list(i)
#print('writing to csv')
sentences, joined = get_word_appended(d)
#d.to_csv('event_arg.csv',sep=',')

with open('../data/linking_arrays/'+args.frame+'.pickle', 'wb') as f:
	pickle.dump(sentences,f)

with open('../data/ui_files/'+args.frame+'.txt', 'w') as f:
	f.write(joined)
#print('done')

#print('extracting argument phrases')

# e = d['event'].tolist()
# event = list(set([inv_class[i+1] for i in e]))
# event.remove('NONE')
#print('EVENTS:',event)

def get_phrase(l,w):
	phrases = []
	r = -1
	while r < len(l):
		ph = []
		t = 0
		z = 0
		r = r+1
		while r  < len(l) and l[r] == 1:
			#try:
			if w[r] == 76171:
				lng = 'p'
			else:
				lng = lang
			#z,f = inv_word[(w[r],lng)]
			z = w[r]
			#except:
			#	z = ""
			ph.append(z)
			# print(ph,r,z)
			r = r + 1
		phrases.append(ph)
		# print(phrases)
	phrases = [x for x in phrases if x != []]
	return phrases


arg_dict = {}
for i in arguments:
	# print('ARGUMENT: ',i)
	z_arg = get_phrase(d[i], d['real_words'].tolist())
	# print(z_arg)
	arg_dict[i] = z_arg
# print("EVENTS", class_predict)
# print(arg_dict)


####FRAME GENERATION
def chunkIt(seq, num):
	avg = len(seq) / float(num)
	out = []
	last = 0.0

	while last < len(seq):
		out.append(seq[int(last):int(last + avg)])
		last += avg

	return out

#print(chunkIt(arg_dict['PLACE-ARG'],2))

frame_dict = {}
event_arg_dict = {}
arg_chunk_dict = {}
n_events = len(class_predict)
for j in arguments:
	arg_chunk_dict[j] = chunkIt(arg_dict[j],2)
for i in range(n_events):
	event_arg_dict[class_predict[i]] = 'A'
	# print(event_arg_dict[class_predict[i]])
	#print(arg_chunk_dict['PLACE-ARG'][i])
	temp_dict = {}
	for j in arguments:
		try:
			temp_dict[j] = arg_chunk_dict[j][i]
		except:
			continue
	event_arg_dict[class_predict[i]] = temp_dict
	#{z: arg_chunk_dict[z][i] for z in  arguments}
print(event_arg_dict)
#print(args.frame)
if bool(event_arg_dict):
	frame_path = '../data/hindi_frames/'+args.frame+'.pickle'
	print("FRAME PATH:",frame_path)
	pickle.dump(event_arg_dict,open('../data/hindi_frames/'+args.frame+'.pickle','wb'))
	print('created frames...')
	os.system("python db_update.py --frame="+args.frame+" --dt="+args.dt+" --tm="+args.tm+" --lang="+args.lang+" --docpath="+args.docpath+" --disp="+args.disp)
else:
	print('no event...')
