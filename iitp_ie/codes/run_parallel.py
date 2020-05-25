import sys
from multiprocessing import Process
from time import sleep
import os
sys.version
import argparse
parser = argparse.ArgumentParser(description='trigger detection classification and argument extraction')

parser.add_argument('--docpath', default="/home/cel/dataset/", type=str, metavar='N', help='doc path')
parser.add_argument('--disp', default="no", type=str, metavar='N', help='no for testing yes for real')

args = parser.parse_args()

lang_dict = {'hi':'hindi','en':'english','bn':'bengali','mr':'marathi'}

Pros = []

def run_extract(i,j):
	print(f'python extract_complete.py --lang= {i} --disp = {args.disp} --docpath = {args.docpath+j}/')
	os.system(f'python extract_complete.py --lang={i} --disp={args.disp} --docpath={args.docpath+j}/manmade_disaster/')

def function_y():
	print("done extraction...")

for i,j in lang_dict.items():
	print("Thread Started for language ",j)
	p = Process(target=run_extract, args=(i,j,))
	Pros.append(p)
	p.start()

for t in Pros:
	t.join()

function_y()