
from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server, static
from twisted.web.resource import Resource
import datetime
import time
import json
 
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

    def __init__(self):
        self.presence=[]
        Resource.__init__(self)

    def render_GET(self, request):
        with open ("login.html", "r+") as myfile:
            data=myfile.read()

        request.write(data)
        self.presence.append(request)
        request.finish()
        return server.NOT_DONE_YET

root = Resource()
root.putChild('', LoginPage())
root.putChild("home.html", ClockPage())
root.putChild("style.css", static.File("style.css"))
root.putChild("bootstrap", static.File("./bootstrap"))
root.putChild("alarms.html", AlarmPage())
factory = Site(root)
reactor.listenTCP(8888, factory)
reactor.run() 
