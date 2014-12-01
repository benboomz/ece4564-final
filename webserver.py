
from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server, static
from twisted.web.resource import Resource
import datetime
import time
import json
 
class ClockPage(Resource):
    isLeaf = 0
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

        return data


root = Resource()
root.putChild('', ClockPage())
root.putChild("style.css", static.File("style.css"))
root.putChild("bootstrap", static.File("./bootstrap"))
root.putChild('alarms.html', AlarmPage())
factory = Site(root)
reactor.listenTCP(8888, factory)
reactor.run() 






'''from twisted.internet import reactor
from twisted.internet import task
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet.protocol import Protocol, Factory

import time

class Echo(Protocol):
    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(data)

class ClockPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        with open ("html.txt", "r") as myfile:
            data=myfile.read()
        old = data.replace("sleepcycles", str(time.ctime()))
        return old


resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)


reactor.run()


from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource
import time
 
class ClockPage(Resource):
    isLeaf = True
    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__print_time)
        loopingCall.start(1, False)
        Resource.__init__(self)
     
    def render_GET(self, request):
        request.write('<b>%s</b><br>' % (time.ctime(),))
        self.presence.append(request)
        return server.NOT_DONE_YET
     
    def __print_time(self):
        for p in self.presence:
            p.write('<b>%s</b><br>' % (time.ctime(),))
 
resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run() 


from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server, rewrite, resource
from twisted.web.resource import Resource
import time
 
class ClockPage(Resource):
    isLeaf = True
    def __init__(self):
        self.presence=[]
        loopingCall = task.LoopingCall(self.__print_time)
        loopingCall.start(1, False)
        Resource.__init__(self)
     
    def render_GET(self, request):
        request.write('<b>%s</b><br>' % (time.ctime(),))
        self.presence.append(request)
        return server.NOT_DONE_YET

    def __print_time(self):
        for p in self.presence:
            rewrite.RewriterResource(p, rewrite.tildeToUsers)

class RewriterResource(resource.Resource):
    def __init__(self, orig, *rewriteRules):
        resource.Resource.__init__(self)
        self.resource = orig
        self.rewriteRules = list(rewriteRules)

    def _rewrite(self, request):
        for rewriteRule in self.rewriteRules:
           rewriteRule(request)

    def getChild(self, path, request):
        request.postpath.insert(0, path)
        request.prepath.pop()
        self._rewrite(request)
        path = request.postpath.pop(0)
        request.prepath.append(path)
        return self.resource.getChildWithDefault(path, request)

    def render(self, request):
        self._rewrite(request)
        return self.resource.render(request)
        
    def tildeToUsers(request):
        if request.postpath and request.postpath[0][:1]=='~':
            request.postpath[:1] = ['users', request.postpath[0][1:]]
            request.path = '/'+'/'.join(request.prepath+request.postpath)
 
resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run() 

'''
