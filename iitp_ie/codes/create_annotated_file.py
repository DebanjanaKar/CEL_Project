import pandas as pd
import json
import numpy as np

def get_word_appended(d):
	d = pd.read_csv('event_arg.csv',sep=',')
	event = [d['event'] != 'NONE']
	words_events = [d['real_words'].loc[i]+'|'+d['event'].loc[i] if event[0][i] else str(d['real_words'].loc[i]) for i in range(len(event[0]))]
	d['word_events'] = words_events
	arg_index = json.load(open("../data/dictionaries/arg_index.json"))
	arguments = [i for i,j in arg_index.items() if i != 'P']
	for z in arguments:
		words_events = [d['word_events'].loc[i]+'|'+z if d[z][i] == 1 else str(d['word_events'].loc[i]) for i in range(len(event[0]))]
		d['word_events'] = words_events

	words_events = [i+'|'+'NONE' if len(i.split('|')) == 1 else i for i in words_events]
	d['word_events'] = words_events
	d.to_csv('test.csv',sep=',',index=False)

	event_words = np.asarray(d['word_events'].tolist())
	event_words = event_words.reshape(-1,75)
	sentences = []
	joined = []
	for i in event_words:
		temp = []
		j_temp = []
		for j in i:
			if j != 'pad|NONE':
				temp.append(j)
		sentences.append(temp)
		j_temp = ' '.join(temp)
		joined.append(j_temp)

	joined_str = '. '.join(joined)+'.'
	#print(joined_str)
	return sentences, joined_str
	
