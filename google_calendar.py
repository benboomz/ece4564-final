import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
	client_id='286518689990-houk6epk8mmpottb3o5ns6c7jfv4iqpq.apps.googleusercontent.com',
	client_secret='MMqETfGzjBk5bPWl7_74E8sK',
	scope='https://www.googleapis.com/auth/calendar',
	user_agent='SMART_ALARM_CLOCK/VER_1.0')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.

# storage = Storage('calendar.dat')
# credentials = storage.get()
# if credentials is None or credentials.invalid == True:
# 	credentials = run(FLOW, storage)


def authorize(credentials):
	# Create an httplib2.Http object to handle our HTTP requests and authorize it
	# with our good Credentials.
	http = httplib2.Http()
	http = credentials.authorize(http)
	return http

def getService():

	storage = Storage('calendar.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid == True:
		credentials = run(FLOW, storage)

	http = authorize(credentials)

	# Build a service object for interacting with the API. Visit
	# the Google Developers Console
	# to get a developerKey for your own application.
	service = build(serviceName='calendar', version='v3', http=http,
	       developerKey='AIzaSyD8_uIwOB3Uo144ZPITdC9TJAwUU8IkTkI')
	return service