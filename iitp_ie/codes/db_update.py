import pandas as pd
from lat_long import loc_resolve
import time
import argparse
import os

parser = argparse.ArgumentParser(description='trigger detection classification and argument extraction')
#parser.add_argument('--doc', default="", type=str, metavar='N', help='file to extract information')
parser.add_argument('--frame', default="4359c55cdb1dffea1d411e7fb0a2c3f1", type=str, metavar='N', help='frame name')
parser.add_argument('--dt', default="2018-12-23", type=str, metavar='N', help='date')
parser.add_argument('--tm', default="14:48", type=str, metavar='N', help='time')
parser.add_argument('--lang', default="hi", type=str, metavar='N', help='language')
parser.add_argument('--docpath', default="../../outside_data/", type=str, metavar='N', help='doc path')
parser.add_argument('--disp', default="no", type=str, metavar='N', help='doc path')

args = parser.parse_args()


import mysql.connector

mydb = mysql.connector.connect(
  host = "localhost.localdomain",
#  proxy = "http://172.16.2.30/",
  user = "root",
  password = "Cel_123!",
  database='cel'
)
disp = args.disp
mycursor = mydb.cursor()

def create_pipes(arguments):
	pipe = ""
	for i in arguments:
		pipe=pipe+"|"+' '.join(j for j in i)
	
	return pipe[1:]

event_arg_dict = pd.read_pickle('../data/hindi_frames/'+args.frame+".pickle")
os.system(f'rm ../data/hindi_frames/{args.frame}.pickle')
#print(event_arg_dict)

for event,argument_dict in event_arg_dict.items():
	#print(event)
	all_arg_names = []
	all_pipes = []
	l_l = ""
	flag = ""
	flag1 = ""
	place = ""
	lang = args.lang
	for arg_name in argument_dict:
		#print(key)
		#print(argument_dict[arg_name])
		#print(arg_name)
		if arg_name == 'PLACE-ARG':
			for z in argument_dict[arg_name]:
				loc = ' '.join(x for x in z)
				#print(loc)
				flag,flag1 = loc_resolve(loc)
				time.sleep(2)
				if flag != -999 and flag1 !=-999:
					l_l=str(flag)+"|"+str(flag1)
					place = loc
					break;
				else:
					l_l = ""
		all_arg_names.append(arg_name)
		p = create_pipes(argument_dict[arg_name])
		#print(p)
		all_pipes.append(p)
	print('EVENT',event)
	print('DOC ID:', args.frame)
	print('date:',args.dt)
	print('time:',args.tm)
	print('LAT-LONG',l_l)
	print("RESOLVED PLACE :",place)
	arg_col_names = [i.replace('-','_') for i in all_arg_names]
	if len(arg_col_names)==0:
		arg_col_names = ""
	else:
		arg_col_names = ",".join(i for i in arg_col_names)
		arg_col_names = ","+arg_col_names
	print('ARG-COL-NAMES',arg_col_names)
	print('ALL-ARGS',all_pipes)
	if len(all_pipes)==0:
		all_pipes = ""
	else:
		all_pipes = ",".join("'"+str(i)+"'" for i in all_pipes)
		all_pipes = ","+all_pipes
	print(all_pipes)
	print('display',disp)
	query = "INSERT INTO master_table (DOCID,EVENT_TYPE,LANGUAGE,DOC_DATE,DOC_TIME,DOC_PATH,DISPLAY,LAT_LONG"+arg_col_names+") VALUES ('"+args.frame+"','"+event+"','"+args.lang+"','"+args.dt+"','"+args.tm+"','"+args.docpath+"','"+disp+"','"+l_l+"'"+all_pipes+")"
	print(query)
	mycursor.execute(query)
	mydb.commit()
  
	
