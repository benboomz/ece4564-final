parsethis = "{u'dateTime': u'2014-11-30T20:00:00-05:00'}"
print parsethis

trimmed = parsethis[16:].replace('T', ' ')
indexofT = trimmed.find('T')
parselist = trimmed.split('-')

month = parselist[1]
datelist = parselist[2].split(' ')
date = datelist[0]
timetemp = datelist[1]
year = parselist[0]

timelist = timetemp.split(":")
hour = timelist[0]
minute = timelist[1]

if int(hour) > 12:
	newhour = str(int(hour) - 12)
	ampm = "PM"
else:
	newhour = hour
	ampm = "AM"


newtime = newhour + ":" + minute + " " + ampm
parseddate = month + "/" + date + "/" + year + " " + newtime
print parseddate

#print trimmed[:indexofT]