import os
import re
from glob import glob
import codecs
from bs4 import BeautifulSoup
from lxml import etree
from date_resolve import d_resolve

import argparse

parser = argparse.ArgumentParser(description='trigger detection classification and argument extraction')
parser.add_argument('--display', default="no", type=str, metavar='N', help='yes/no yes for real and no for testing')
parser.add_argument('--lang', default="hi", type=str, metavar='N', help='language')
parser.add_argument('--docpath', default="../../outside_data", type=str, metavar='N', help='path of crawled files')

args = parser.parse_args()

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

#path = '../outside_data/*'
path = args.docpath+'/*'
file_list = glob(path)
#display = "no"
display = args.display
#lang='hi'
lang = args.lang

#text_files=[]
#####



#file_list = ['../outside_data/0c060e75a8f4e2b08aeda443b6d08b0f.xml']
for i in file_list:
	text_file=""


	with codecs.open(i, encoding='utf-8') as file:
		text_file = file.read()


	soup = BeautifulSoup(text_file)
	try:
		docId = soup.docid.string
		print("DOCID=",docId)
		date_time = soup.date.string.split(',')[-1]
		print("DATE TIME=",date_time)
		print("enter try")
		dt,tm = d_resolve(date_time)
		print(dt,tm)
	#doc_id = docId.value
	#print(doc_id)

		total_text = str(soup.title.string)+" "+str(soup.article.string)
		print(total_text)
		text_file = remove_html_tags(text_file)
		#text_file = text_file.replace('\n',' ')
		temp_file = "../data/temp/"+i.split('/')[-1]
		with open(temp_file, "w") as text_file:
			text_file.write(total_text)
		print("ARGS.FRAME",i.split('/')[-1].split('.')[0])
		os.system("python extract_event_argument.py --doc="+temp_file+" --frame="+i.split('/')[-1].split('.')[0]+ " --tm="+str(tm)+" --dt="+str(dt)+" --docpath="+str(i)+" --disp="+display+" --lang="+lang)
		os.system("rm "+temp_file)
	except:
		print("some error in file (possibly could not resolve date-time)...")

