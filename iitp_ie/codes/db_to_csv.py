import mysql.connector
import csv

mydb = mysql.connector.connect(
  host = "localhost.localdomain",
  user = "root",
  password = "Cel_123!",
  database='cel'
)

mycursor = mydb.cursor()


query = "SELECT * from master_table"
header = ['DOCID','EVENTID','EVENT_TYPE','LANGUAGE','DOC_DATE','DOC_TIME','DOC_PATH','TIME_ARG','PLACE_ARG','REASON_ARG','CASUALTIES_ARG','TYPE_ARG','PARTICIPANT_ARG','INTENSITY_ARG','MAGNITUDE_ARG','NAME_ARG','SPEED_ARG','DEPTH_ARG','AFTER_EFFECTS_ARG','TEMPERATURE_ARG','EPICENTRE_ARG','LAT_LONG','DISPLAY']
mycursor.execute(query)

with open('dump.csv','w') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for row in mycursor.fetchall():
		writer.writerow(row)

mydb.commit()
