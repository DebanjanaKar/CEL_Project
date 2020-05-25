from geopy.geocoders import Nominatim
from googletrans import Translator

def loc_resolve(loc_name):
	geolocator = Nominatim(user_agent="CELProject")
	translator = Translator()
	l = translator.translate(loc_name).text

#	loc_name = "பாட்னா"
	location = geolocator.geocode(l)
	try:
		return location.latitude,location.longitude
	except:
		return -999,-999
