calendarId = 'teamdanier@gmail.com'

import google_calendar
from datetime import datetime 
import pprint

def getEvents(pageToken=None):
    events = google_calendar.service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2013-11-30T00:00:00-08:00', #str(datetime.now.isoformat()),
        timeMax='2015-11-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events

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

print "Events: "
events = getEvents()
while True:
    for event in events['items']:
        pprint.pprint(event['summary'])
        pprint.pprint(event['start'])
    page_token = events.get('nextPageToken')
    if page_token:
        events = getEvents(page_token)
        print events
    else:
        break
