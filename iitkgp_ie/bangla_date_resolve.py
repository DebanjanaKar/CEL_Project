from shared_ie import date_resolve
def resolve_date(st):
	month =	{" জানুয়ারী": "January", " ফেব্রুয়ারী": "February", " মার্চ": "March", "এপ্রিল": "April", "মে": "May", "জুন": "June", "জুলাই": "July", " আগস্ট ": "August", "সেপ্টেম্বর": "September", "অক্টোবর": "October", "নভেম্বর": "November", "ডিসেম্বর": "December"}
	st_list = st.split()
	for index,i in enumerate(st_list):
		i = i.replace('.','').replace('/','').replace(',','').replace('-','').strip()
		if i in month.keys():
			st_list[index]=month[i]
	out_str=" ".join([x for x in st_list])		
	final_str = date_resolve.d_resolve(out_str)
	return final_str
	
