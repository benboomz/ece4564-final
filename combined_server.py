calendarId = 'teamdanier@gmail.com'

import google_calendar
from datetime import tzinfo, timedelta, datetime
import pprint
import time as _time
from threading import Thread
from adxl345 import ADXL345

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

ZERO = timedelta(0)
DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):
    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0


def getEvents(pageToken=None):
    events = google_calendar.getService().events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin=str(datetime.now(LocalTimezone()).isoformat('T')),
        timeMax='2015-11-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events

def parsestring(stringtoparse):
    if "dateTime" in stringtoparse:
        trimmed = stringtoparse[16:].replace('T', ' ')
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
        return parseddate
    else:
        return ""

def accelerometer():
    adxl345 = ADXL345()

    count = 1

    xsum = 0.0
    ysum = 0.0
    zsum = 0.0

    minx = miny = minz = 100
    maxx = maxy = maxz = -100
    print


    while 1:    

        time.ctime()
        hour = time.strftime("%H")
        minute = time.strftime("%M")

        minutetrigger = 0
        if minute == "00":
            minutetrigger = 1
        else:
            minutetrigger = 0

        if hour > 22 or hour < 10:
            hourtrigger = 1

        # if it is between 10 pm and 10 am, and the minute is 00, start reading from accelerometer
        # the accelerometer will average the amount of movements from each axis for every hour
        while minutetrigger and hourtrigger:

            axes = adxl345.getAxes(True)
            
            x = axes['x']
            y = axes['y']
            z = axes['z']
            
            count = count + 1   
            xsum = xsum + x
            ysum = ysum + y
            zsum = zsum + z
                
            if x < minx:
                minx = x
            if y < miny:
                miny = y
            if z < minz:
                minz = z

            if x > maxx:
                maxx = x
            if y > maxy:
                maxy = y
            if z > maxz:
                maxz = z

            #count = 600 is a minute
            # 36000 is an hour
            if count == 36000:
                count = 1
                xavg = xsum / 36000.0
                yavg = ysum / 36000.0
                zavg = zsum / 36000.0
                
                xavg = round(xavg, 2)
                yavg = round(yavg, 2)
                zavg = round(zavg, 2)
                minx = round(minx, 2)
                miny = round(miny, 2)
                minz = round(minz, 2)
                maxx = round(maxx, 2)
                maxy = round(maxy, 2)
                maxz = round(maxz, 2)
                
                rangex = maxx - minx
                rangey = maxy - miny
                rangez = maxz - minz

                avgrange = round((rangex+rangey+rangez)/3, 2)
                
                if avgrange > 0.50:
                    print "red"
                elif avgrange < 0.20:
                    print "green"
                else:
                    print "yellow"

                print "\t" + str(avgrange)
                print "\t" + str(rangex), str(rangey), str(rangez)
                print       
        

                xsum = ysum = zsum = 0
                minx = miny = minz = 100
                maxx = maxy = maxz = -100

            if hour == 10:
                hourtrigger = 0

            time.sleep(0.1) 


# def calendar_events():
#     print "Events: "
#     events = getEvents()
#     while True:
#         for event in events['items']:
#             pprint.pprint(event)
#         page_token = events.get('nextPageToken')
#         if page_token:
#             events = getEvents(page_token)
#             print events
#         else:
#             break

# if __name__ == '__calendar_events__':
#     calendar_events()

while 1:

    # get events from the google calendar
    events = getEvents()
    listofevents = ""
    while True:

        for event in events['items']:
            pprint.pprint(event['summary'])
            pprint.pprint(event['start'])
            listofevents = listofevents + str(event['start']) + '\n'
            print ''
        page_token = events.get('nextPageToken')
        if page_token:
            events = getEvents(page_token)
            print events
        else:
            break

    listofeventslist = listofevents.split("\n")
    neweventlist = ""
    for times in listofeventslist:
        if parsestring(times) != "":
            neweventlist = neweventlist + parsestring(times) + "\n"

    # write alarms into alarms.txt - makes sure not to repeat
    with open("alarms.txt") as f:
        alarmlist = f.readlines()

    with open("alarms.txt", "w") as f:
        f.write(neweventlist)
        for alarms in alarmlist:
    	   if alarms in neweventlist:
                pass
    	   else:
                f.write(alarms)

    # next few lines of codes sorts the alarm
    with open("alarms.txt") as f:
        alarmlist = f.readlines()

    alarmlist = sorted(alarmlist)

    with open("alarms.txt", "w") as f:
        for alarms in alarmlist:
            f.write(alarms)


    time.ctime()
    currenttime = time.strftime('%m/%d/%Y%l:%M %p') #11/30/14 5:34 PM
    print currenttime

    for alarms in alarmlist:
        if alarms.strip() == currenttime.strip():
            pygame.mixer.init()
            pygame.mixer.music.load("alarm_beep.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            


    time.sleep(60)
