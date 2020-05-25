import pandas as pd
from lat_long import loc_resolve

import argparse

parser = argparse.ArgumentParser(description='trigger detection classification and argument extraction')
parser.add_argument('--doc', default="", type=str, metavar='N', help='file to extract information')
parser.add_argument('--frame', default="4359c55cdb1dffea1d411e7fb0a2c3f1", type=str, metavar='N', help='frame name')
parser.add_argument('--dt', default="", type=str, metavar='N', help='date')
parser.add_argument('--tm', default="", type=str, metavar='N', help='time')
args = parser.parse_args()

def create_pipes(arguments):
	pipe = ""
	for i in arguments:
		pipe=pipe+"|"+' '.join(j for j in i)
	
	return pipe[1:]
event_arg_dict = pd.read_pickle('test.pickle')
#print(event_arg_dict)

for event,argument_dict in event_arg_dict.items():
	#print(event)
	all_arg_names = []
	all_pipes = []
	l_l = ""
	flag = ""
	flag1 = ""
	for arg_name in argument_dict:
		#print(key)
		#print(argument_dict[arg_name])
		#print(arg_name)
		if arg_name == 'PLACE-ARG':
			for z in argument_dict[arg_name]:
				loc = ' '.join(x for x in z)
				#print(loc)
				flag,flag1 = loc_resolve(loc)
				if flag != -999 and flag1 !=-999:
					l_l=str(flag)+","+str(flag1)
					break;
				else:
					l_l = ""
		all_arg_names.append(arg_name)
		p = create_pipes(argument_dict[arg_name])
		#print(p)
		all_pipes.append(p)
	print(event)
	print(l_l)
	print(all_arg_names)
	print(all_pipes)
