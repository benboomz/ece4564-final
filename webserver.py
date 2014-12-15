from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server, static
from twisted.web.resource import Resource

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import gflags
import google_calendar

import datetime
import time
import json
import cgi
import os
 
class ClockPage(Resource):
    isLeaf = 1
    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        with open ("home.html", "r+") as myfile:
            data=myfile.read()
        
        with open("sleephistory.json", "r+") as historyfile:
            sleep_history = json.load(historyfile)
            html = ""
            
            for day in sorted(sleep_history.keys()):
                html += '''<div class="row"><div class="col-md-2 date">''' + day + "</div>"

                for time in sorted(sleep_history[day].keys()):
                    html += '''<div class="col-md-1">
                                <div class="circle circle-border"'''

                    status = sleep_history[day][time]
                    if status == "awake":
                        html += '''style="border: 2px solid #FF0000;">'''
                    elif status == "light sleep":
                        html += '''style="border: 2px solid #FFFF00;">'''
                    elif status == "rem sleep":
                        html += '''style="border: 2px solid #31B404;">'''

                    html += '''<div class="circle-inner"><div class="hour-text">''' + time
                    html += '''             </div>
                                        </div>
                                    </div>
                                </div>'''
                html += "</div>"

        new = data.replace("sleepcycles", str(html))
        request.write(new)
        self.presence.append(request)
        request.finish()
        return server.NOT_DONE_YET

    def getChild(self, path, request):
        if path == '':
            return self
        elif path == 'alarms.html':
            return AlarmPage()

class AlarmPage(Resource):
    isLeaf = 1

    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        with open ("alarms.html", "r+") as myfile:
            data=myfile.read()

        with open("alarms.txt", "r+") as alarmfile:
            alarmlist = alarmfile.readlines()
            html = ""
        for alarms in alarmlist:
            html += '''<div class="row">''' + alarms + "</div"
            html += "<br>"


        new = data.replace("sleepcycles", str(html))
        request.write(new)
        self.presence.append(request)
        request.finish()
        return server.NOT_DONE_YET

class LoginPage(Resource):
    isLeaf = 0
    allowedMethods = ('GET', 'POST')
	
    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        if not os.path.isfile("calendar.dat"):
            storage = Storage('calendar.dat')
            credentials = storage.get()

            if credentials is None or credentials.invalid == True:
                with open ("login.html", "r+") as myfile:
                    data=myfile.read()

                request.write(data)
                self.presence.append(request)
                request.finish()
                return server.NOT_DONE_YET
        else:
            request.redirect("/home.html")
            request.finish()
            return server.NOT_DONE_YET
    
    def render_POST(self, request):

        if "signin" in request.args:
            authorize_url = FLOW.step1_get_authorize_url()
            request.redirect(str(authorize_url))
            request.finish()
            return server.NOT_DONE_YET

        if "code" in request.args:
            try: 
                credentials = FLOW.step2_exchange(cgi.escape(request.args["code"][0]))
                # storage = Storage('calendar.dat')
                # credentials = storage.get()
                # if credentials is None or credentials.invalid == True:
                #     credentials = run(FLOW, storage)

                storage = Storage('calendar.dat')
                storage.put(credentials)
                print "Stored credentials in calendar.dat"

                google_calendar.authorize(credentials)
            except:
                print "User already authorized."

            request.redirect("/home.html")
            request.finish()
            return server.NOT_DONE_YET

class LogoutPage(Resource):
    isLeaf = True

    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        if os.path.isfile("calendar.dat"):
            os.remove("calendar.dat")

        with open ("logout.html", "r+") as myfile:
            data=myfile.read()
            request.write(data)
            self.presence.append(request)
            request.finish()
            return server.NOT_DONE_YET

class CreateAlarmPage(Resource):
    isLeaf = True

    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        with open("createalarm.html", "r+") as myfile:
            data=myfile.read()
            request.write(data)
            self.presence.append(request)
            request.finish()
            return server.NOT_DONE_YET




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
    user_agent='SMART_ALARM_CLOCK/VER_1.0',
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

root = Resource()
root.putChild('', LoginPage())
root.putChild("home.html", ClockPage())
root.putChild("alarms.html", AlarmPage())
root.putChild("logout.html", LogoutPage())
root.putChild("style.css", static.File("style.css"))
root.putChild("bootstrap", static.File("./bootstrap"))
factory = Site(root)
reactor.listenTCP(8888, factory)
reactor.run() 
