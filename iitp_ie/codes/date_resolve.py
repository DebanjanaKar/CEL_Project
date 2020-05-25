from dateutil.parser import parse
import json
from googletrans import Translator

def d_resolve(date_str):
	month_dict = json.load(open("../../shared_ie/month_dict.json"))
	#print(month_dict)
	z = date_str.split()
	month_list = [i for i,j in month_dict.items()]
	en_date = ' '.join(month_dict[i] if i in month_list else i for i in z)
	#translator = Translator()
	#en_date = translator.translate(date_str).text
	print(en_date)
	#d = date_str.split()
	#d_m = []
	#for i in d:
	#	try:
	#		d_m.append(month_dict[i])
	#	except:
	#		d_m.append(i)
	#final_str = " ".join(i for i in d_m)
	#print(final_str)
	try:
		full_date_time = parse(en_date,fuzzy_with_tokens=True)			
	#print(str(full_date_time[0]).split()[0])
		return str(full_date_time[0]).split()[0], str(full_date_time[0]).split()[1]
	except:
		return ""



