import pandas as pd
import json

d = pd.read_csv('event_arg.csv',sep=',')
#time = d['TIME-ARG'].tolist()
arg_dict = {}
arguments = d.columns[3:]



class_index = json.load(open("../data/dictionaries/class_index.json"))
arg_index = json.load(open("../data/dictionaries/arg_index.json"))
word_index = pd.read_pickle("../data/dictionaries/universal_word_index.pickle")
lang = 'hi'

inv_class = {v: k for k, v in class_index.items()}
inv_arg = {v: k for k, v in arg_index.items()}
inv_word = {v: k for k, v in word_index.items()}

e = d['event'].tolist()
event = list(set([inv_class[i+1] for i in e]))
event.remove('NONE')
print('EVENTS:',event)

def get_phrase(l,w):
  phrases = []
  r = -1
  while r < len(l):
    ph = []
    t = 0
    z = 0
    r = r+1
    while r  < len(l) and l[r] == 1:
      z,f = inv_word[(w[r],lang)]
      ph.append(z)
      r=r+1
    phrases.append(ph)
  phrases = [x for x in phrases if x != []]
  return phrases



for i in arguments:
  print('ARGUMENT: ',i)
  print(get_phrase(d[i],d['words'].tolist()))
